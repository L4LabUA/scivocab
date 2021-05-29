#!/usr/bin/env python
# coding: utf-8

# First, get database from server.
# 
# 1. Make a copy of the old app.db if you want.
# 2. Double click on clickable script copy_scivocab_db_from_server (in this folder) - that will download the database to your computer.
# 3. Run the commands below. 

# In[14]:


import pandas as pd
from typing import List, Dict
from sqlalchemy import create_engine

import matplotlib.pyplot as plt

# Increase the maximum number of rows displayed to 999
pd.options.display.max_rows=999

# Connect to the database
engine = create_engine("sqlite:///app.db")

def construct_dfs() -> Dict:
    """Create a dictionary of dataframes, keyed by task name"""
    dfs: Dict = {}

    # Populate the dictionary with the dfs
    dfs["breadth"] = pd.read_sql(
        """select
            child_id,
            word.id as word_id,
            breadth_id,
            strand_id,
            word.target as target_word,
            response_type,
            position,
            timestamp
        from breadth_response
        inner join word on 
        breadth_response.word_id=word.id;""",
        engine,
        parse_dates=["timestamp"]
    )

    dfs["depth"] = pd.read_sql(
        """select
            child_id,
            word.id as word_id,
            depth_id,
            strand_id,
            word.target as target_word,
            image_0,
            image_1,
            image_2,
            image_3,
            timestamp
        from depth_response
        inner join word on 
        depth_response.word_id=word.id;""",
        engine,
        parse_dates=["timestamp"]
    )

    dfs["definition"] = pd.read_sql(
        """select
            child_id,
            word.id as word_id,
            definition_id,
            strand_id,
            word.target as target_word,
            text,
            timestamp
        from definition_response
        inner join word on
        definition_response.word_id=word.id;""",
        engine,
        parse_dates=["timestamp"]
    )

    return dfs


def postprocess_depth_df(df) -> None:
    """Replace d..._X.jpg with X in the image_N columns"""
    for i in range(4):
        df[f"image_{i}"] = (
            df[f"image_{i}"].str.split("_").str[1].str.split(".").str[0]
        )


def calculate_depth_item_score(df):
    """Calculate the score for each depth task response"""
    return (
        sum(
            [
                df[f"image_{index}"] == code
                for index, code in zip((0, 1, 2, 3),
                                       ("a", "b", "c", "e"))
            ]
        )
        / 4
    )

def make_depth_fractions_df(dfs):
    """Make a dataframe showing the fractions of depth task image
    types that the participants got correct"""
    records=[]

    for child_id, df in dfs["depth"].groupby(["child_id"]):
        df = df[df["strand_id"] != "training"]
        record = {"child_id": child_id}
        for index, code in zip((0, 1, 2, 3), ("a", "b", "c", "e")):
            filtered = df[f"image_{index}"] == code
            record.update(
                {f"fraction of {code}'s correct" : filtered.sum() / filtered.count()})
        records.append(record)

    result_df = pd.DataFrame(records)
    return result_df


# In[15]:


dfs = construct_dfs()
postprocess_depth_df(dfs["depth"])
dfs["depth"]["score"] = calculate_depth_item_score(dfs["depth"])


# In[16]:


# Show the breadth task responses
dfs["breadth"]

# In[17]:


# Show the depth task responses
dfs["depth"]


# In[18]:


# Show the definition task responses
dfs["definition"]


# In[19]:


# Make the fractions dataframe
fractions_df=make_depth_fractions_df(dfs)

fractions_df.to_csv("Depth_Fraction_df.csv", sep="\t")

# Show the fractions dataframe
fractions_df


# In[20]:


# Set plot style
plt.style.use("ggplot")


# In[29]:


# Histograms of response times by task and item
# Note: This does not take into account the time spent in the fun facts (which is low, but still)
fig, axes = plt.subplots(1, 3, figsize=(12,4))
for i, task in enumerate(("breadth", "depth", "definition")):
    response_times = [
        (((dfs[task].loc[row.Index]["timestamp"]
         - dfs[task].loc[row.Index-1]["timestamp"]).seconds)/60)
        for row in dfs[task].itertuples()
        if row.strand_id != "training"
    ]
    axes[i].hist(response_times, label=f"{task} response times")
    axes[i].set_xlabel("Item response time (m)")
    axes[i].set_title(task.capitalize())

plt.tight_layout()

plt.savefig("Histogram_of_response_times.pdf")

# In[27]:


# Bar plots of total times taken for tasks
import numpy as np
fig, axes = plt.subplots(1, 3, figsize=(12, 4), sharey=True)
tasks=("breadth", "depth", "definition")
axes[0].set_ylabel("Task duration (m)")

for i, task in enumerate(tasks):
    timedeltas = []
    child_ids=[]
    for child_id, responses in dfs[task].groupby("child_id"):
        timedelta=(((responses.loc[responses.index[-1]]["timestamp"]
              - responses.loc[responses.index[0]]["timestamp"]).seconds)/60)
        timedeltas.append(timedelta)
        child_ids.append(child_id)
    index = np.arange(len(timedeltas))
    axes[i].bar(index, timedeltas, tick_label=child_ids)
    axes[i].set_xlabel("Child ID")
    axes[i].set_title(task.capitalize())
    
plt.tight_layout()


# In[ ]:

plt.savefig("Bar_Graph_Total_Times.pdf")



# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





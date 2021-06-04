#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
from typing import List, Dict
from sqlalchemy import create_engine

import matplotlib.pyplot as plt

# Connect to the database
engine = create_engine("sqlite:///../app/app.db")

# Set plot style
plt.style.use("ggplot")


def calculate_depth_item_score(df):
    """Calculate the score for each depth task response"""
    return (
        sum(
            [
                df[f"image_{index}"] == code
                for index, code in zip((0, 1, 2, 3), ("a", "b", "c", "e"))
            ]
        )
        / 4
    )


def postprocess_depth_df(df) -> None:
    """Replace d..._X.jpg with X in the image_N columns"""
    for i in range(4):
        df[f"image_{i}"] = (
            df[f"image_{i}"].str.split("_").str[1].str.split(".").str[0]
        )
    df["score"] = calculate_depth_item_score(df)


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
        parse_dates=["timestamp"],
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
        parse_dates=["timestamp"],
    )

    dfs["definition"] = pd.read_sql(
        """select
            child_id,
            word.id as word_id,
            definition_id,
            strand_id,
            word.target as target_word,
            text,
            score,
            timestamp
        from definition_response
        inner join word on
        definition_response.word_id=word.id;""",
        engine,
        parse_dates=["timestamp"],
    )

    postprocess_depth_df(dfs["depth"])
    dfs["breadth"]["score"] = dfs["breadth"]["response_type"] == "tw"

    return dfs


def make_depth_fractions_df(dfs):
    """Make a dataframe showing the fractions of depth task image
    types that the participants got correct"""
    records = []

    for child_id, df in dfs["depth"].groupby(["child_id"]):
        df = df[df["strand_id"] != "training"]
        record = {"child_id": child_id}
        for index, code in zip((0, 1, 2, 3), ("a", "b", "c", "e")):
            filtered = df[f"image_{index}"] == code
            record.update(
                {
                    f"fraction of {code}'s correct": filtered.sum()
                    / filtered.count()
                }
            )
        records.append(record)

    result_df = pd.DataFrame(records)
    return result_df


def make_fractions_df(dfs):
    # Make the fractions dataframe
    fractions_df = make_depth_fractions_df(dfs)
    fractions_df.to_csv("Depth_Fraction_df.csv", sep="\t")


def make_response_times_histo(dfs):
    # Histograms of response times by task and item
    # Note: This does not take into account the time spent in the fun facts
    # (which is low, but still)
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    for i, task in enumerate(("breadth", "depth", "definition")):
        response_times = [
            (
                (
                    dfs[task].loc[row.Index]["timestamp"]
                    - dfs[task].loc[row.Index - 1]["timestamp"]
                ).seconds
            )
            for row in dfs[task].itertuples()
            if row.strand_id != "training"
        ]
        axes[i].hist(response_times, label=f"{task} response times")
        axes[i].set_ylabel("Number of items")
        axes[i].set_xlabel("Item response time (s)")
        axes[i].set_title(task.capitalize())

    plt.tight_layout()
    plt.savefig("Histogram_of_response_times.pdf")


def make_total_times_bar_plot(dfs):
    # Bar plots of total times taken for tasks
    fig, axes = plt.subplots(1, 3, figsize=(12, 4), sharey=True)
    tasks = ("breadth", "depth", "definition")
    axes[0].set_ylabel("Task duration (m)")

    for i, task in enumerate(tasks):
        timedeltas = []
        child_ids = []
        for child_id, responses in dfs[task].groupby("child_id"):
            timedelta = (
                (
                    responses.loc[responses.index[-1]]["timestamp"]
                    - responses.loc[responses.index[0]]["timestamp"]
                ).seconds
            ) / 60
            timedeltas.append(timedelta)
            child_ids.append(child_id)
        index = np.arange(len(timedeltas))
        color = [
            "RoyalBlue" if child_id.startswith("9") else "firebrick"
            for child_id in child_ids
        ]
        axes[i].bar(index, timedeltas, color=color, tick_label=child_ids)
        axes[i].set_xlabel("Child ID")
        axes[i].set_title(task.capitalize())

    plt.tight_layout()
    plt.savefig("Bar_Graph_Total_Times.pdf")


def make_total_score_plot(dfs):
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))
    max_scores = {"breadth": 108, "depth": 48, "definition": 80}

    for i, task in enumerate(("breadth", "depth", "definition")):
        total_scores = []
        child_ids = []
        for child_id, responses in dfs[task].dropna().groupby("child_id"):
            if child_id == "1003" and task == "definition":
                print(responses)
            child_ids.append(child_id)
            total_scores.append(responses["score"].sum())

        index = np.arange(len(child_ids))
        color = [
            "RoyalBlue" if child_id.startswith("9") else "firebrick"
            for child_id in child_ids
        ]
        axes[i].bar(index, total_scores, tick_label=child_ids, color=color)
        axes[i].set_title(task.capitalize())
        axes[i].set_ylim(0, max_scores[task])
        axes[i].set_xlabel("Child ID")
        axes[i].set_ylabel("Score")

    plt.tight_layout()
    plt.savefig("total_scores.pdf")


def make_score_dist_plot(dfs):
    fig, axes = plt.subplots(1, 2, figsize=(8, 4))

    tick_labels = {"depth": (0, 0.25, 0.5, 1), "definition": (0, 1, 2, 3, 4)}
    # Depth task
    for i, task in enumerate(("depth", "definition")):
        score_count_pairs = [
            (score, len(group))
            for score, group in dfs[task][
                dfs[task]["child_id"] != "1003"
            ].groupby("score")
        ]

        scores, counts = zip(*score_count_pairs)
        index = np.arange(len(scores))
        axes[i].bar(index, counts, tick_label=tick_labels[task])
        axes[i].set_title(task.capitalize())
        axes[i].set_label("Score")
        axes[i].set_xlabel("Score")
        axes[i].set_ylabel("Number of responses")

    plt.tight_layout()
    plt.savefig("response_score_distribution.pdf")


if __name__ == "__main__":
    dfs = construct_dfs()
    make_response_times_histo(dfs)
    make_total_times_bar_plot(dfs)
    make_total_score_plot(dfs)
    make_score_dist_plot(dfs)
    make_fractions_df(dfs)

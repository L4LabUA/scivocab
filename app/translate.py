from pandas import read_csv
from app.word import Word

# construct_word_dict takes in a filename for an excel sheet that is a list of words for input
# (see excel file flask/status/scivocab/sv_bv1_input for the format.)
# For each seperate name in target, it creates a word datatype.
# Finally, it returns a dictionary of all created word datatypes.

def construct_word_dict(filename):
    allWords = dict()
    df = read_csv(filename)
    for name, group in df.groupby("target"):
        allWords[name] = Word(
            group["strand"].iloc[0], group["breadth_id"].iloc[0], name
        )
        for i, row in group.iterrows():
            setattr(
                allWords[name], str(row["img_type"]), int(row["position"][1])
            )
    return allWords


# get_filename takes a word and id to translate into the format in which the images are saved- see the file sv_bv1.
def get_filename(word, id):
    return f"scivocab/sv_bv1/bv1_{word.id}_p{getattr(word, id)}_{id}.jpg"

from pandas import read_csv
from word import Word


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


# Translates a word to return
def get_filename(word, id):
    return f"scivocab/sv_bv1/bv1_{word.id}_p{getattr(word, id)}_{id}.jpg"

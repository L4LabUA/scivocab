import pandas
<<<<<<< HEAD
from flask import WordConstruct





def main():
    allWords = dict()
    graphinput = pandas.read_csv("static/scivocab/sv_bv1_input.csv")
    for index, row in graphinput.iterrows():
        if row['target'] in allWords:
            # The key already exists. That means we just need to input which it is.
            print(allWords[row['target']].fw)
        else:
            allWords[row['target']] = WordConstruct.Word()
            allWords[row['target']].fw = 1



=======


class Word:

    def __init__(self):
        self.tw = -1
        self.fp = -1
        self.fx = -1
        self.fs = -1
        self.strand = -1
        self.target = ''
        self.id = -1


def main():
    x = pandas.read_csv("static/scivocab/sv_bv1_input.csv")
>>>>>>> SamTest



main()

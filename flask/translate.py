import pandas
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







main()

import pandas
from flask import WordConstruct


def main(args):
    allWords = dict()
    graphinput = pandas.read_csv(args)
    for index, row in graphinput.iterrows():
        if row['target'] not in allWords:
            # The key doesn't exist. We need to define a new dictionary piece for it.
            allWords[row['target']] = WordConstruct.Word()
            allWords[row['target']].strand = row['strand']
            allWords[row['target']].id = row['breadth_id']
            allWords[row['target']].target = row['target']
        # Now, we figure out which image we're looking at
        if row['img_type'] == 'tw':
            allWords[row['target']].tw = int(row['position'][1])
        if row['img_type'] == 'fp':
            allWords[row['target']].fp = int(row['position'][1])
        if row['img_type'] == 'fx':
            allWords[row['target']].fx = int(row['position'][1])
        if row['img_type'] == 'fs':
            allWords[row['target']].fs = int(row['position'][1])
    # or x in allWords:
        # print(toimage(allWords[x], 'tw'))
        # print(x + ' has its true word in position ' + str(allWords[x].tw) + " and is part of strand " + str(allWords[x].strand))


# Translates a word to return
def toimage(word, id):
    if id == 'tw':
        return "bv1_" + word.id + "_p" + str(word.tw) + "_tw.jpg"


# main("static/scivocab/sv_bv1_input.csv")






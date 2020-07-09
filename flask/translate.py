import pandas
from flask import WordConstruct



def main():
    allWords = dict()
    graphinput = pandas.read_csv("static/scivocab/sv_bv1_input.csv")
    for index, row in graphinput.iterrows():
        if row['target'] not in allWords:
            # The key doesn't exist. We need to define a new dictionary piece for it.
            allWords[row['target']] = WordConstruct.Word()
            allWords[row['target']].strand = row['strand']
            allWords[row['target']].id = row['breadth_id']
        # Now, we figure out which image we're looking at
        if row['img_type'] == 'tw':
            allWords[row['target']].tw = int(row['position'][1])
        if row['img_type'] == 'fp':
            allWords[row['target']].fp = int(row['position'][1])
        if row['img_type'] == 'fx':
            allWords[row['target']].fx = int(row['position'][1])
        if row['img_type'] == 'fs':
            allWords[row['target']].fs = int(row['position'][1])
    #for x in allWords:
        #print(x + ' has its true word in position ' + str(allWords[x].tw) + " and is part of strand " + str(allWords[x].strand))










main()

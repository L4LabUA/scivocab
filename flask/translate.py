import pandas
from word import Word

def main(filename):
    allWords = dict()
    df = pandas.read_csv(filename)
    for index, row in df.iterrows():
        print(row)
        if row['target'] not in allWords:
            # The key doesn't exist. We need to define a new dictionary piece for it.
            allWords[row['target']] = Word()
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
    return allWords


# Translates a word to return
def toimage(word, id):
    if id == 'tw':
        return "scivocab/sv_bv1/bv1_" + word.id + "_p" + str(word.tw) + "_tw.jpg"
    if id == 'fp':
        return "scivocab/sv_bv1/bv1_" + word.id + "_p" + str(word.fp) + "_fp.jpg"
    if id == 'fx':
        return "scivocab/sv_bv1/bv1_" + word.id + "_p" + str(word.fx) + "_fx.jpg"
    if id == 'fs':
        return "scivocab/sv_bv1/bv1_" + word.id + "_p" + str(word.fs) + "_fs.jpg"

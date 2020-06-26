import pandas


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



main()

# A class that stores all the information needed by the researcher after the program is done.
class Answer:

    def __init__(self, word, answer, strand):
        self.word = word
        # the name of the word (target)
        self.answer = answer
        # tw, fp, fx, or fs, whichever the user selected. Stored as a string.
        self.strand = strand
        # which strand the word belonged to. Stored as an int.

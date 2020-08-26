#  A class that stores all the information needed to make one set of images associated with a target.


class Word:

    def __init__(self, strand, id, target):
        self.tw = -1
        self.fp = -1
        self.fx = -1
        self.fs = -1
        # the position each of these identifications is stored in-
        # images are labelled 1 to 4, but one set may have tw in position 3 and fp in position 1, while another
        # may have fp in 3 and tw in 1
        self.strand = strand
        # the strand number (identifies which science category it belongs to)
        self.target = target
        # the name of the word (target)
        self.id = id
        # linked to what test this word is attached to. (Breadth or Depth- specifically bv1 and dv1)

    # calling word.identify(num) will return the identification of any numbered image.
    # word.identify(3) will return the value of the image in position 3.
    def identify(self, num):
        if num == None:
            return
        num = int(num[5])
        if self.tw == num:
            return 'tw'
        if self.fp == num:
            return 'fp'
        if self.fx == num:
            return 'fx'
        if self.fs == num:
            return 'fs'
        return 'error'

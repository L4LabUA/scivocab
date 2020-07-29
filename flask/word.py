class Word:

    def __init__(self, strand, id, target):
        self.tw = -1
        self.fp = -1
        self.fx = -1
        self.fs = -1
        self.strand = strand
        self.target = target
        self.id = id

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

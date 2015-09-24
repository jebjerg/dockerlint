class Peep(object):
    def __init__(self, l):
        self.ls = l
        self.i = 0

    def next(self):
        if self.i >= len(self.ls):
            raise StopIteration
        v = self.ls[self.i]
        self.i += 1
        return v

    def peak(self, ahead=0):
        if self.i+ahead >= len(self.ls):
            raise StopIteration
        val = self.ls[self.i+ahead]
        if not val:
            return ("EOF", "")
        return val

    def last(self):
        return self.peak(-1)

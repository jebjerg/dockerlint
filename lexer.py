import symbols

class Lexer(object):
    def __init__(self, text):
        self.start = 0
        self.pos = 0
        self.text = text

    def emit(self, t):
        if self.pos >= len(self.text):
            return
        if self.pos > self.start:
            val = self.text[self.start:self.pos]
            self.start = self.pos
            return (t, val)

    @property
    def buf(self):
        if self.pos > self.start:
            return self.text[self.start:self.pos]
        return ""

    @property
    def curr(self):
        if self.pos >= len(self.text):
            return False
        return self.text[self.pos]

    def accept(self, chars):
        for c in self.next_char():
            if not self.curr or self.curr not in chars:
                break

    def accept_until(self, chars):
        for c in self.next_char():
            if not self.curr or self.curr in chars:
                break

    def next_char(self):
        while self.pos < len(self.text):
            val = self.text[self.pos]
            self.pos += 1
            yield val

    def next_token(self):
        while self.curr:
            if self.curr == symbols.COMMENT:
                while self.accept_until(symbols.NEWLINE):
                    pass
                self.accept(symbols.NEWLINE)
                yield self.emit("COMMENT")
            elif self.curr == symbols.COMMA:
                self.accept(symbols.COMMA)
                yield self.emit("COMMA")
            elif self.curr in symbols.STRING_LITERALS:
                sl = self.curr
                while self.accept_until(sl):
                    pass
                self.accept(sl)
                yield self.emit("STRING")
            elif self.curr in symbols.SQUARE_OPEN:
                self.accept(symbols.SQUARE_OPEN)
                yield self.emit("BRACKET_OPEN")
            elif self.curr in symbols.SQUARE_CLOSE:
                self.accept(symbols.SQUARE_CLOSE)
                yield self.emit("BRACKET_CLOSE")
            elif self.curr in symbols.VALID_CHARS:
                while self.accept(symbols.VALID_CHARS):
                    pass
            elif self.curr in symbols.WHITESPACE:
                while self.accept(symbols.WHITESPACE):
                    pass
                yield self.emit("WHITESPACE")
            elif self.curr in symbols.NEWLINE:
                while self.accept(symbols.NEWLINE):
                    pass
                yield self.emit("NEWLINE")

            if self.buf in symbols.KEYWORDS:
                yield self.emit("KEYWORD")
            else:
                t = self.emit("TEXT")
                if t:
                    yield t

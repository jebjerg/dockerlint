from symbols import KEYWORDS_JSON_SUPPORT
from utils import Peep
from lexer import Lexer
from ast import Steps, Step


class Parser(object):
    def expect(self, *a, **kw):
        t, _ = self.tokens.peak()
        if t == "EOF":
            return False
        if t in list(a) + [v for k, v in kw.iteritems()]:
            self.tokens.next()
            return True
        return False

    def expect_not(self, *a, **kw):
        t, _ = self.tokens.peak()
        if t == "EOF":
            return False
        if t not in list(a) + [v for k, v in kw.iteritems()]:
            self.tokens.next()
            return True
        return False

    def must(self, *a, **kw):
        t, _ = self.tokens.peak()
        if t in list(a) + [v for k, v in kw.iteritems()]:
            self.tokens.next()
            return True
        raise Exception(
            "Expected {}, but got {}".format(
                ",".join(list(a) + [v for k, v in kw.iteritems()]), t
            )
        )

    def must_be(self, typ, val):
        t, v = self.tokens.peak()
        if t == typ and v == val:
            self.tokens.next()
            return True
        raise Exception(
            "Expected {} ({}), but got {} ({})".format(
                val, typ,
                v, t,
            )
        )

    def parse(self, text):
        self.lexer = Lexer(text)
        self.tokens = Peep([t for t in self.lexer.next_token()])

        ast = Steps()

        retval = self.instruction()
        assert retval and retval.instruction == "FROM"
        while retval:  # read instructions
            if type(retval) != bool:
                ast.steps.append(retval)
            retval = self.instruction()

        return ast

    def instruction(self):
        while self.expect("WHITESPACE"):
            pass
        if self.expect("NEWLINE"):
            return True
        step = Step()
        if self.expect("COMMENT"):
            return True
        elif self.expect("KEYWORD"):
            step.instruction = self.tokens.last()[1]
            self.expect("WHITESPACE")

            if step.instruction in KEYWORDS_JSON_SUPPORT \
                    and self.expect("BRACKET_OPEN"):
                # expect json array
                self.must("STRING")
                step.arguments.append(self.tokens.last()[1])
                while self.expect("COMMA"):
                    self.expect("WHITESPACE")
                    self.must("STRING")
                    step.arguments.append(self.tokens.last()[1])
                    self.expect("WHITESPACE")
                self.must("BRACKET_CLOSE")
                while self.expect("WHITESPACE"):
                    pass
                self.expect("NEWLINE")
            else:
                while self.expect_not("NEWLINE"):
                    if self.tokens.last()[0] == "WHITESPACE":  # skip spaces
                        continue
                    step.arguments.append(self.tokens.last()[1])
                self.expect("NEWLINE")
            return step
        return False

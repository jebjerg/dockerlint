from string import letters


KEYWORDS_JSON_SUPPORT = [
    "ENTRYPOINT",
    "VOLUME",
    "RUN",
    "CMD",
    "ADD",
    "COPY",
]

KEYWORDS = [
    "FROM", "MAINTAINER",
    "LABEL",
    "EXPOSE",
    "ENV",
    "USER",
    "WORKDIR",
    "ONBUILD",
] + KEYWORDS_JSON_SUPPORT

VALID_CHARS = letters + "0123456789" + "-_"

WHITESPACE = [
    " ",
    "\t",
]

NEWLINE = "\n"

COMMENT = "#"

COMMA = ","

STRING_LITERALS = "\""

SQUARE_OPEN = "["
SQUARE_CLOSE = "]"
BRACKETS = SQUARE_OPEN + SQUARE_CLOSE

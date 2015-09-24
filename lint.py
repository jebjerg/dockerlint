from parser import Parser
from sys import stdin, exit
from os import getenv
# TODO: lint class and logic

# for now: simple, but easy to expand.
# return codes:
# 0: parse ok, lint ok
# 1: parse ok, lint w/ warnings
# 2: parse failed, lint skipped
# 3: parse ok, lint errs
if __name__ == "__main__":
    p = Parser()
    try:
        ast = p.parse(stdin.read())
    except Exception as e:  # syntax errors
        print e
        exit(2)

    # sanity check/lint
    def warn(*a):
        global warns
        warns += 1
        print "WARN!", " ".join(a)

    debug = getenv("DEBUG")
    if debug:
        print ast

    warns = 0
    errs = 0

    user = "root"
    for step in ast.steps:
        if debug:
            print "STEP", step.instruction, "=>", step.arguments
        if step.instruction == "USER":
            assert len(step.arguments) == 1
            user = step.arguments[0]
        if step.instruction == "RUN" \
                and "lol" in step.arguments \
                and (not user or user == "root"):
            warn("don't do this as root: " + str(step))
    if errs:
        exit(3)
    elif warns:
        exit(1)
    else:
        exit(0)

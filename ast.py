class Steps(object):
    def __init__(self):
        self.steps = []

    def __repr__(self):
        return "\n".join([str(step) for step in self.steps])


class Step(object):
    def __init__(self):
        self.instruction = None
        self.arguments = []

    def __repr__(self):
        return " ".join([self.instruction] + self.arguments)

class BaseEval:
    def __init__(self, methods: list):
        self.methods = methods

    def run(self, predictions: list, labels: list):
        raise NotImplementedError
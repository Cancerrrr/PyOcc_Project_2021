


class Standard_ConstructionError(RuntimeError):
    def __init__(self, arg):
        self.args = arg
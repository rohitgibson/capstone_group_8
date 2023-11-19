from os import makedirs

class MiscUtils:
    def __init__(self):
        pass

    def createPath(self, path:str):
        try:
            makedirs(path)
        except OSError:
            pass

        
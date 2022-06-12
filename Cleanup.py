import os


class Cleanup:
    def __init__(self, files: str):
        self.listdir = os.listdir(files)
        for item in self.listdir:
            if item.endswith(".mp3") or item.endswith(".wav") or item.endswith(".txt"):
                os.remove(os.path.join(files, item))

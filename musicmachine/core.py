import toml


class MusicMachine:

    def __init__(self):
        self.queue = []

    @property
    def config(self):
        c = toml.load('config.toml', _dict=dict)
        return c

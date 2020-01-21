import toml


class MusicMachine:

    @property
    def config(self):
        c = toml.load('config.toml', _dict=dict)
        return c
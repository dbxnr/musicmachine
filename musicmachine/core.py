import toml


class BandcampRadio:

    @property
    def config(self):
        c = toml.load('config.toml', _dict=dict)
        return c
from core import MusicMachine
from web.explorer import Explorer
from player.player import Player


x = MusicMachine()
while True:
    y = Explorer(x)
    z = Player(y.track['media_url'], y.track['duration']).play()

from core import BandcampRadio
from web.explorer import Explorer
from player.player import Player
from player.player import Display

from curses import wrapper

x = BandcampRadio()
y = Explorer(x)
z = Player(y.track['media_url'], y.track['duration']).play()

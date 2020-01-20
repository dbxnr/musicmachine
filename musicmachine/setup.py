from core import BandcampRadio
from web.explorer import Explorer
from player.player import Player

x = BandcampRadio()
y = Explorer(x)
z = Player(y.track['media_url']).play()
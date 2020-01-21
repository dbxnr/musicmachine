import threading
import time

from core import MusicMachine
from web.explorer import Explorer
from player.player import Player


x = MusicMachine()


def build_queue():
    while len(x.queue) < 2:
        x.queue.append(Explorer(x))


if __name__ == "__main__":
    while True:
        if len(x.queue) == 0:
            x.queue.append(Explorer(x))
        else:
            z = threading.Thread(target=Player(x.queue[0]
                                               .track['media_url'],x.queue[-1]
                                               .track['duration']).play)
            y = threading.Thread(target=build_queue)
            y.start()
            z.start()
            time.sleep(x.queue[0].track['duration'])

            x.queue.pop(0)

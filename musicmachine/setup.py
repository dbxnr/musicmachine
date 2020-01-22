import threading
import time

from core import MusicMachine
from web.explorer import Explorer
from player.player import Player
from ui.display import Display

import warnings
warnings.filterwarnings("ignore")


x = MusicMachine()


def build_queue():
    while len(x.queue) < 2:
        x.queue.append(Explorer(x))


if __name__ == "__main__":
    while True:
        if len(x.queue) == 0:
            x.queue.append(Explorer(x))
        else:
            # Possibly use multiprocessing instead to eliminate stutter?
            z = threading.Thread(target=Player(x.queue[0]
                                               .track['media_url'],
                                               x.queue[0]
                                               .track['duration'])
                                 .play)
            y = threading.Thread(target=build_queue)
            d = Display(x.queue[0].selected_tag,
                        x.queue[0].artist['band_name'],
                        x.queue[0].album['album_name'],
                        x.queue[0].track['track_name'])
            print(vars(d))
            d = threading.Thread(target=d.main)
            y.start()
            z.start()
            d.start()
            time.sleep(x.queue[0].track['duration'])

            x.queue.pop(0)

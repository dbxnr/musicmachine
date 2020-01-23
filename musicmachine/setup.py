import threading
import time

from core import MusicMachine
from web.explorer import Explorer
from player.player import Player
from ui.display import Display

q_length = 3

x = MusicMachine()
d = Display()


def build_queue(num):
    while len(x.queue) < num:
        x.queue.append(Explorer(x))


if __name__ == "__main__":
    while True:
        if len(x.queue) == 0:
            # Could add a progress bar here
            print('Buffering tracks...')
            build_queue(q_length)
        else:
            z = threading.Thread(target=Player(x.queue[0]
                                               .track['media_url'],
                                               x.queue[0]
                                               .track['duration'])
                                 .play)
            y = threading.Thread(target=build_queue, args=([q_length]))
            d.set_track_info(
                x.queue[0].selected_tag,
                x.queue[0].artist['band_name'],
                x.queue[0].album['album_name'],
                x.queue[0].track['track_name'],
                x.queue[0].track['duration']
                )
            dt = threading.Thread(target=d.main)
            y.start()
            z.start()
            dt.start()
            z.join()

            x.queue.pop(0)

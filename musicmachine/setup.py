import multiprocessing
import threading

from core import MusicMachine
from web.explorer import Explorer
from player.player import Player
from ui.display import Display

q_length = 3


def build_queue(num):
    while len(x.queue) < num:
        x.queue.append(Explorer(x))


if __name__ == "__main__":
    x = MusicMachine()
    d = Display()

    print('Buffering tracks...')
    while d.running:
        if len(x.queue) == 0:
            for i in range(q_length):
                p = threading.Thread(target=build_queue(1))
                p.start()
        else:
            z = multiprocessing.Process(target=Player(x.queue[0]
                                               .track['media_url'],
                                               x.queue[0]
                                               .track['duration'])
                                 .play)
            y = multiprocessing.Process(target=build_queue, args=([q_length]))
            d.set_track_info(
                x.queue[0].selected_tag,
                x.queue[0].artist['band_name'],
                x.queue[0].album['album_name'],
                x.queue[0].track['track_name'],
                x.queue[0].track['duration'],
                )
            dt = multiprocessing.Process(target=d.main)
            # user_input = threading.Thread(target=d.detect_keypress)
            # user_input.start()
            dt.start()
            y.start()
            z.start()
            z.join()

            x.queue.pop(0)

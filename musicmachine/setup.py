import sys
import termios
import threading
import time
import tty

from multiprocessing import Process, Queue

from core import MusicMachine
from web.explorer import Explorer
from player.player import Player
from ui.display import Display

q_length = 1


def getch():
    # Adapted from https://stackoverflow.com/a/47069232
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def get_keypress(q):
    while audio_stream.is_alive():
        key = getch()
        if key == "q":
            exit()
        q.put(key)


def build_queue(num):
    while len(x.queue) < num:
        x.queue.append(Explorer(x))


if __name__ == "__main__":
    x = MusicMachine()
    display = Display()

    print("Buffering tracks...")
    while display.running:
        if len(x.queue) == 0:
            processes = []
            for _ in range(q_length):
                p = threading.Thread(target=build_queue, args=(1,))
                p.start()
                processes.append(p)
            for process in processes:
                process.join()
        else:
            q = Queue()
            audio_stream = Process(
                target=Player(
                    x.queue[0].track["media_url"], x.queue[0].track["duration"]
                ).play
            )
            queue_builder = Process(target=build_queue, args=([q_length]))
            display.set_track_info(
                x.queue[0].selected_tag,
                x.queue[0].artist["band_name"],
                x.queue[0].album["album_name"],
                x.queue[0].track["track_name"],
                x.queue[0].track["duration"],
            )
            display_proc = Process(target=display.main, args=(q,))
            display_proc.start()
            queue_builder.start()
            audio_stream.start()
            user_input = threading.Thread(target=get_keypress, args=(q,))
            user_input.start()
            audio_stream.join()
            x.queue.pop(0)

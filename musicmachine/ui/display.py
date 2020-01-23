import re
import termios
import tty
import sys
import time
from tqdm import tqdm, trange

class Display:
    def __init__(self, tag, artist, album, track, duration):
        self.tag = tag
        self.artist = artist
        self.album = album
        self.track = track
        self.duration = duration

    def main(self):

        print(f"Artist:\t{self.artist}\t\tAlbum:\t{self.album}\t\tTrack:\t{self.track}\r")
        for i in trange(int(self.duration)):
            time.sleep(1)

    @staticmethod
    def getpos():
        # From https://stackoverflow.com/a/46677968

        buf = ""
        stdin = sys.stdin.fileno()
        tattr = termios.tcgetattr(stdin)

        try:
            tty.setcbreak(stdin, termios.TCSANOW)
            sys.stdout.write("\x1b[6n")
            sys.stdout.flush()

            while True:
                buf += sys.stdin.read(1)
                if buf[-1] == "R":
                    break

        finally:
            termios.tcsetattr(stdin, termios.TCSANOW, tattr)

        # reading the actual values, but what if a keystroke appears while reading
        # from stdin? As dirty work around, getpos() returns if this fails: None
        try:
            matches = re.match(r"^\x1b\[(\d*);(\d*)R", buf)
            groups = matches.groups()
        except AttributeError:
            return None

        return (int(groups[0]), int(groups[1]))
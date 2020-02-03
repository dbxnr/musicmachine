import re
import sys
import termios
import time
import tty

from tqdm import tqdm, trange
from tqdm.utils import _unicode


class Display:
    def __init__(self):
        self.tag: str = ''
        self.artist: str = ''
        self.album: str = ''
        self.track: str = ''
        self.duration: float = 0.0
        self.cursor_pos: tuple = ()

        print('\n')

        if not self.cursor_pos:
            self.cursor_pos = self.getpos()

        tqdm.status_printer = self.status_printer

    def set_track_info(self, tag, artist, album, track, duration) -> None:
        self.tag: str = tag
        self.artist: str = '👩‍🎤  ' + artist
        self.album: str = '💿  ' + album
        self.track: str = '🎵  ' + track
        self.duration: float = duration

    def main(self) -> None:
        # Clear line
        sys.stdout.write(f"\033[{self.cursor_pos[0]-2};0H\033[K")
        # Put cursor in position and print track info
        sys.stdout.write(f"\033[{self.cursor_pos[0]-2};0H  {self.artist:<25} {self.album:<30} {self.track:<30}  \r")

        for i in trange(int(self.duration), 
                            bar_format='  [{percentage:3.0f}%] {bar} | 👍  [{remaining}]  ',
                            ascii = [' ', '▶', '▷', '▹', '▸'],
                            mininterval=0.05):
            time.sleep(1)

    @staticmethod
    def getpos() -> tuple:
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

    # Override tqdm.status_printer()
    def status_printer(self, file):
        """
        Manage the printing and in-place updating of a line of characters.
        Note that if the string is longer than a line, then in-place
        updating may not work (it will print a new line at each refresh).
        """
        fp = file
        fp_flush = getattr(fp, 'flush', lambda: None)  # pragma: no cover

        def fp_write(s):
            fp.write(_unicode(s))
            fp_flush()

        last_len = [0]

        def print_status(s):
            len_s = len(s)
            fp_write(f"\033[{self.cursor_pos[0]-1};0H" + s + (' ' * max(last_len[0] - len_s, 0)))
            last_len[0] = len_s

        return print_status

    @staticmethod
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

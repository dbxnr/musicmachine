import time


class Display:
    def __init__(self, tag, artist, album, track):
        self.tag = tag
        self.artist = artist
        self.album = album
        self.track = track

    def write_info(self):
        self.stdscr = self.addstr(0, 0, self.tag)
        self.stdscr = self.addstr(2, 0, self.artist)
        self.stdscr = self.addstr(4, 0, self.album)
        self.stdscr = self.addstr(4, 0, self.track)

    def main(self):
        for x in (self.artist, self.album, self.track):
            print(x + '\n')

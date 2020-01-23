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

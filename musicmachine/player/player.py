import miniaudio
import requests
import time


class Player:
    def __init__(self, stream, duration):
        self.stream = stream
        self.duration = duration

    def play(self):
        s = requests.get(self.stream, stream=True).raw

        channels = 2
        sample_rate = 44100

        stream = miniaudio.stream_any(source=s,
                                      source_format=miniaudio.FileFormat.MP3,
                                      nchannels=channels,
                                      sample_rate=sample_rate)
        device = miniaudio.PlaybackDevice()
        device.start(stream)
        time.sleep(self.duration+1)
        device.close()
        return True


class Display:
    def __init__(self, tag, artist, album, track):
        self.tag = tag
        self.artist = artist
        self.album = album
        self.track = track

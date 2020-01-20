import miniaudio
import requests


class Player:
    def __init__(self, stream):
        self.stream = stream

    def play(self):
        s = requests.get(self.stream, stream=True).raw

        channels = 2
        sample_rate = 44100

        stream = miniaudio.stream_any(source=s, source_format=miniaudio.FileFormat.MP3, nchannels=channels, sample_rate=sample_rate)
        device = miniaudio.PlaybackDevice()
        device.start(stream)
        input("Audio file playing in the background. Enter to stop playback: ")
        device.close()

import miniaudio
import requests
import time


import warnings


class Player:
    def __init__(self, stream, duration):
        self.stream: str = stream
        self.duration: float = duration
        self.media: HttpResponse = requests.get(self.stream, stream=True).raw
        self.run: bool = True

    def play(self) -> bool:
        channels: int = 2
        sample_rate: int = 44100
        device = miniaudio.PlaybackDevice()

        stream = miniaudio.stream_any(source=self.media,
                                      source_format=miniaudio.FileFormat.MP3,
                                      nchannels=channels,
                                      sample_rate=sample_rate)

        device.start(stream)
        time.sleep(self.duration)
        self.run = False
            
        device.close()
        return True

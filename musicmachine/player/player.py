import miniaudio
import requests
import time


class Player:
    def __init__(self, stream, duration):
        self.stream: str = stream
        self.duration: float = duration

    def play(self) -> bool:
        try:
            media = requests.get(self.stream, stream=True).raw
        except requests.exceptions.MissingSchema:
            return False

        channels: int = 2
        sample_rate: int = 44100
        device = miniaudio.PlaybackDevice()

        stream = miniaudio.stream_any(
            source=media,
            source_format=miniaudio.FileFormat.MP3,
            nchannels=channels,
            sample_rate=sample_rate,
        )

        device.start(stream)
        time.sleep(self.duration)
        device.close()
        return True

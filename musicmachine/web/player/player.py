import miniaudio
import requests


file = 'https://files.freemusicarchive.org/storage-freemusicarchive-org/music/no_curator/KieLoKaz/Free_Ganymed/KieLoKaz_-_02_-_Trip_to_Ganymed_Kielokaz_ID_363.mp3'
s = requests.get(file, stream=True).raw

channels = 2
sample_rate = 44100

stream = miniaudio.stream_any(source=s, source_format=miniaudio.FileFormat.MP3, nchannels=channels, sample_rate=sample_rate)
device = miniaudio.PlaybackDevice()
device.start(stream)
input("Audio file playing in the background. Enter to stop playback: ")
device.close()

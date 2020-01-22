import json
import random
import re

from datetime import datetime
from typing import Callable, List, Union, Dict

import requests

from bs4 import BeautifulSoup


class Explorer:
    def __init__(self, radio):
        self.config = radio.config

        self.tags = set()
        self.selected_tag = ''
        self.artist: Dict = {}
        self.album: Dict[str] = {'album_name': '',
                                 'album_url': ''}

        self.track: Dict[Union[str, float]] = {'track_name': '',
                                               'track_url': '',
                                               'duration': 0.0,
                                               'media_url': ''}

        self.setup()

    def setup(self) -> None:
        self.get_tags()
        self.clean_tags()
        self.selected_tag = self.random_selection(self.tags)
        self.get_random_artist(self.selected_tag)
        self.get_random_album()
        self.get_random_track()

    @staticmethod
    def is_it_christmas() -> bool:
        return datetime.now().month == 11 | datetime.now().month == 11

    @staticmethod
    def random_selection(choices) -> Union[str, dict]:
        choice: str = random.choice(tuple(choices))
        return choice

    def get_tags(self) -> bool:
        tags: List[str] = []
        r = requests.get(self.config['BASE_URL']+self.config['TAGS'])
        s = BeautifulSoup(r.text, 'lxml')
        result = s.find_all(id='tags_cloud')

        for e in result:
            tags.extend(e.get_text()
                        .lstrip()
                        .replace(' ', '-')
                        .splitlines())
        self.tags = set(tags)

        return True

    def clean_tags(self) -> bool:
        """
        Handler for some bad data that could be
        removed earlier in the pipeline.
        """
        try:
            self.tags.remove('view-all')
            self.tags.remove('')
            if not self.is_it_christmas():
                self.tags.remove('christmas')
            return True
        except KeyError:
            return False

    def get_random_artist(self, tag) -> Union[bool, Callable]:
        # This could be a user param, popularity range(x,y)
        page: int = random.randint(1, 35)
        body: str = '"tags":["' + tag + '"]},"page":' + str(page) + '}'

        r = requests.post(url=self.config['DIG_DEEPER'],
                          headers=self.config['HEADERS'],
                          data=self.config['BODY']+body,
                          stream=True)

        data: str = json.loads(r.text)
        try:
            artist: Dict = dict(data['items'][random.randint(0, len(data['items']))])
            self.artist = artist
            return True

        except Exception as e:
            #print(f'Still choosing from {self.selected_tag}', e)
            return self.get_random_artist(self.selected_tag)

    def get_random_album(self) -> Union[bool, callable]:
        r = requests.get(self.artist['band_url']+'/music/',
                         headers=self.config['HEADERS'])
        s = BeautifulSoup(r.text, 'lxml')

        albums = list([a['href'] for a in s.select(self.config['ALBUM_SELECTOR'])])
        if len(albums) > 0:
            # Sometimes a url will be /album/ or /track/
            # regex to look into this!
            self.album['album_url'] = self.artist['band_url'] + self.random_selection(albums)
            return True
        else:
            # Pretty serious bug, needs to be investigate
            #print(f"Perusing back catalogues of {self.artist['band_url']}...")
            return self.setup()

    def get_random_track(self) -> Union[bool, callable]:
        # This could be refactored out, a random media url
        # be grabbed from the array of tracks on the album page

        # The track may not contain the selected_tag,
        # BC seems to group artists by all tags used.

        r = requests.get(self.album['album_url'],
                         headers=self.config['HEADERS'])

        s = BeautifulSoup(r.content, 'lxml')
        album_selector = s.select(self.config['ALBUM_NAME_SELECTOR'])

        try:
            self.album['album_name'] = album_selector[0].string.strip()
        except Exception as e:
            return self.get_random_album()
            #print(e)

        tracks = list(a['href'] for a in s.select(self.config['TRACK_SELECTOR']))

        if len(tracks) > 0:
            # Sometimes a url will be /album/ or /track/
            # regex to fix this!
            self.track['track_url'] = self.artist['band_url'] + self.random_selection(tracks)
            self.get_media_data(s)
            return True
        else:
            # Pretty serious bug, needs to be investigated
            #print('Failure', self.artist['band_url'], self.album['album_url'])
            return self.get_random_album()

    def get_media_data(self, soup) -> bool:
        s = soup

        # Kind of hacky, regex could be improved
        try:
            data = json.loads(re.search(r'(trackinfo:)(.[^\]]+])',
                                        s.get_text())
                              .group()[11:])
            track: dict = self.random_selection(data)

            self.track['track_url']: str = self.artist['band_url'] + track['title_link']
            self.track['media_url']: str = track['file']['mp3-128']
            self.track['duration']: float = float(track['duration'])
            self.track['track_name']: str = track['title']

        except Exception as e:
            #print('Get media error', e)
            return self.setup()

        return True

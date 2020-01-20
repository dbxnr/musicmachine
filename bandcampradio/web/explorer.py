import json
import random
import re
from typing import Callable, List, Union

import requests

from bs4 import BeautifulSoup


class Explorer:
    def __init__(self, radio):
        self.config = radio.config

        self.tags = set()
        self.selected_tag = ''
        self.artist = {}
        self.album = {'album_name': '',
                      'album_url': ''}

        self.track = {'track_name': '',
                      'track_url': '',
                      'duration': '',
                      'media_url': ''}

        self.setup()

    def setup(self):
        self.get_tags()
        self.clean_tags()
        self.selected_tag = self.random_selection(self.tags)
        self.get_random_artist(self.selected_tag)
        self.get_random_album()
        self.get_random_track()
        print(self.track['track_url'])
        self.play()

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
            return True
        except KeyError:
            return False

    @staticmethod
    def random_selection(choices) -> tuple:
        choice = random.choice(tuple(choices))
        return choice

    def get_random_artist(self, tag) -> Union[bool, Callable]:
        page = random.randint(1, 25)
        body = '"tags":["' + tag + '"]},"page":' + str(page) + '}'

        r = requests.post(url=self.config['DIG_DEEPER'],
                          headers=self.config['HEADERS'],
                          data=self.config['BODY']+body,
                          stream=True)

        data = json.loads(r.text)
        try:
            artist = data['items'][random.randint(0, len(data['items']))]
            self.artist = artist
            return True

        except Exception as e:
            print(f'Still choosing from {self.selected_tag}')
            return self.get_random_artist(self.selected_tag)

    def get_random_album(self) -> Union[bool, callable]:
        r = requests.get(self.artist['band_url']+'/music/')
        s = BeautifulSoup(r.content, 'lxml')

        albums = list([a['href'] for a in s.select(self.config['ALBUM_SELECTOR'])])

        if len(albums) > 0:
            # Sometimes a url will be /album/ or /track/
            # regex to look into this!
            self.album['album_url'] = self.artist['band_url'] + self.random_selection(albums)
            return True
        else:
            print(f"Perusing back catalogues of {self.artist['band_url']}...")
            return self.get_random_album()

    def get_random_track(self) -> Union[bool, callable]:
        # This could be refactored out, a random media url
        # be grabbed from the array of tracks on the album page

        r = requests.get(self.album['album_url'])
        s = BeautifulSoup(r.content, 'lxml')

        album_selector = s.select(self.config['ALBUM_NAME_SELECTOR'])

        try:
            self.album['album_name'] = album_selector[0].string.strip()
        except Exception as e:
            print(e)

        tracks = list(a['href'] for a in s.select(self.config['TRACK_SELECTOR']))

        if len(tracks) > 0:
            # Sometimes a url will be /album/ or /track/
            # regex to fix this!
            self.track['track_url'] = self.artist['band_url'] + self.random_selection(tracks)
            self.get_media_url(s)
            return True
        else:
            print('Failure', self.artist['band_url'], self.album['album_url'])
            return self.get_random_track()

    def get_media_url(self, request) -> bool:
        s = BeautifulSoup(request.text, 'lxml')
        script = s.find('script', type='text/javascript').get_text()

        # Kind of hacky, regex could be improved
        self.track['media_url'] = re.search(r'(?:"mp3-128":).[^"]+', script).group()[11:]

        return True

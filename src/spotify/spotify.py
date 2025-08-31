import json
import pathlib
from datetime import datetime
from typing import Generator

from spotipy import Spotify, SpotifyOAuth, SpotifyClientCredentials

from .spotify_song import SpotifySong


class SpotifyAPI:
    def __init__(self, data_path: pathlib.Path, cli_login: bool = False):
        scope = 'user-library-read'
        self.api = Spotify(
            auth_manager=SpotifyOAuth(scope=scope, redirect_uri='http://127.0.0.1:8080/', open_browser=not cli_login),
            client_credentials_manager=SpotifyClientCredentials(),
        )

        self.songs_json_path = data_path / 'songs.json'

    def _load_liked_songs(self) -> Generator[SpotifySong, None, None]:
        offset, limit = 0, 50
        while True:
            songs_batch = self.api.current_user_saved_tracks(offset=offset, limit=limit)['items']
            if not songs_batch:
                break  # End of liked songs

            for song in songs_batch:
                added_at = song['added_at']
                added_at = datetime.strptime(added_at, "%Y-%m-%dT%H:%M:%SZ")

                track_data = song['track']

                uri = track_data['uri']

                artists_data = track_data['artists']
                artists = [
                    artist['name']
                    for artist in artists_data
                ]

                song_name = track_data['name']

                album_images = track_data['album']['images']

                album_image_url, album_image_size = None, 0
                # Pick the album image with the largest size
                for image in album_images:
                    curr_image_size = image['width'] * image['height']
                    if curr_image_size > album_image_size:
                        album_image_url = image['url']  # This one fits better
                        album_image_size = curr_image_size

                album_name = track_data['album']['name']
                album_release_year = int(track_data['album']['release_date'][:4])

                yield SpotifySong(
                    uri=uri,
                    added_at=added_at,
                    artists=artists,
                    title=song_name,
                    album_name=album_name,
                    album_image_url=album_image_url,
                    isrc=track_data['external_ids']['isrc'],
                    year=album_release_year,
                )

            offset += limit

    def refresh_saved_liked_songs(self) -> list[SpotifySong]:
        songs: set[SpotifySong] = set()
        for song in self._load_liked_songs():
            songs.add(song)
            print(f'\rFound {len(songs)} songs.', end='')
        print()

        # Save the songs in an appropriate JSON
        with self.songs_json_path.open('w', encoding='UTF-8') as file:
            file: 'SupportsWrite'[str]  # Leave a type hint (TextIO supports str write)
            json.dump([song.__dict__() for song in songs], file, indent=2)

        return list(songs)

    def load_cached_liked_songs(self) -> list[SpotifySong]:
        with self.songs_json_path.open('r', encoding='UTF-8') as file:
            songs = json.load(file)
            return [
                SpotifySong.from_dict(json_entry)
                for json_entry in songs
            ]

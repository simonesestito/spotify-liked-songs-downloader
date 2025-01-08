from ytmusicapi import YTMusic

from ..spotify import SpotifySong
from .youtube_song import YouTubeSong
from ..spotify.utils import normalize_string


class YouTubeMusicSearch:
    def __init__(self):
        self.yt = YTMusic()

    def search(self, song: SpotifySong) -> YouTubeSong | None:
        query = f'{song.title} - {" ".join(song.artists)}'
        results = self.yt.search(
            query=query,
            filter='songs',
            limit=1,
        )

        if not results:
            return None

        result = results[0]
        result_id = result['videoId']

        result_title = normalize_string(result['title'], non_ascii_placeholder='').lower()
        original_title = normalize_string(song.title, non_ascii_placeholder='').lower()

        if result_title != original_title:
            print(f'WARN: downloading a potentially different song')
            print(f'\tOriginal title: {song.title}')
            print(f'\tWhat we found: {result["title"]} (https://youtube.com/watch?v={result_id})')
            print(f'\tPlease manually check if they differ.')

        return YouTubeSong(
            id=result_id,
            info=song,
        )

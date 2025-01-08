from src.lyrics.lrclib import LRCLibLyrics
from src.spotify import SpotifySong


class LyricsAPI:
    def __init__(self):
        self.lrclib = LRCLibLyrics()

    def search_song(self, song_info: SpotifySong) -> str | None:
        found_lyrics = self.lrclib.query_lyrics(
            track_name=song_info.simplified_title,
            artist_name=song_info.artists[0],
        )

        if found_lyrics is not None:
            print(f'WARN: unable to find lyrics for "{song_info.simplified_title} ({song_info.artists[0]})"')

        return found_lyrics

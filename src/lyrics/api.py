import syncedlyrics

from src.spotify import SpotifySong


class LyricsAPI:
    def __init__(self):
        pass

    # noinspection PyMethodMayBeStatic
    def search_song(self, song_info: SpotifySong) -> str | None:
        song_query = f'{song_info.simplified_title} {song_info.artists[0]}'
        song_result = syncedlyrics.search(search_term=song_query,
                                          providers=['lrclib', 'netease', 'genius'])
        if song_result is None:
            print(f'WARN: unable to find lyrics for "{song_query}"')
            return None

        return song_result

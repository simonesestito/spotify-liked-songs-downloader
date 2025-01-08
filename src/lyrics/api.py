import syncedlyrics

from src.spotify import SpotifySong


class LyricsAPI:
    def __init__(self):
        pass

    # noinspection PyMethodMayBeStatic
    def search_song(self, song_info: SpotifySong) -> str | None:
        song_result = syncedlyrics.search(search_term=f'{song_info.simplified_title} {song_info.artists[0]}',
                                          providers=['lrclib', 'netease', 'megalobiz', 'genius'])
        if song_result is None:
            print(f'WARN: unable to find lyrics for "{song_info.title}"')
            return None

        return song_result

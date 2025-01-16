import pathlib

from src.metadata import TagsEmbedder
from src.spotify import SpotifySong


class LocalQuery:
    scanned_songs: dict[str, pathlib.Path]

    def __init__(self, music_dir: pathlib.Path):
        self.music_dir = music_dir
        self._scan_music_dir()

    def _scan_music_dir(self):
        self.scanned_songs = dict()

        for music_file in self.music_dir.iterdir():
            isrc = TagsEmbedder.get_isrc_for_file(music_file)
            if isrc:
                self.scanned_songs[isrc] = music_file

    def find_file_for_song(self, song: SpotifySong) -> pathlib.Path | None:
        """
        Search the song by the ISRC embedded in file's metadata.
        """
        return self.scanned_songs.get(song.isrc, None)

    def delete_unused_songs(self, liked_songs: list[SpotifySong]) -> None:
        isrc_to_keep = { song.isrc for song in liked_songs }

        for stored_isrc, song_file in self.scanned_songs.items():
            if stored_isrc not in isrc_to_keep:
                song_file.unlink(missing_ok=True)

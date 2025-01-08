import pathlib
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from src.spotify.utils import normalize_string


@dataclass
class SpotifySong:
    added_at: datetime

    artists: list[str]
    title: str

    album_name: str
    album_image_url: str|None

    isrc: str
    year: int

    @staticmethod
    def from_dict(json: dict[str, Any]) -> "SpotifySong":
        return SpotifySong(
            added_at=datetime.fromisoformat(json["added_at"]),
            artists=json["artists"],
            title=json["title"],
            album_name=json["album_name"],
            album_image_url=json["album_image_url"],
            isrc=json["isrc"],
            year=json["year"],
        )

    @property
    def normalized_title(self) -> str:
        return normalize_string(self.title)

    @property
    def normalized_artists(self) -> list[str]:
        return [ normalize_string(artist) for artist in self.artists ]

    def filename(self, extension: str | None = 'm4a', with_index: int | None = None) -> str:
        artists = ', '.join(self.normalized_artists)

        # Prefix
        numbered_prefix = '' if with_index is None else f'{with_index:04d} - '

        # Normalize the extension
        if extension and extension[0] != '.':
            extension = '.' + extension
        elif not extension:
            extension = ''

        return f'{numbered_prefix}{self.normalized_title} - {artists}{extension}'


    def exists_in_folder(self, folder: pathlib.Path, extension: str | None = 'm4a') -> pathlib.Path | None:
        simple_filename = self.filename(extension=extension)

        possible_matches = [
            file
            for file in folder.iterdir()
            if file.is_file() and file.name.endswith(simple_filename)
        ]

        # Is there exactly this file?
        if simple_filename in [file.name for file in possible_matches]:
            return next(file for file in possible_matches if file.name == simple_filename)

        # Is there another file, with a numbered index prefix? Obtained by -S option
        for match in possible_matches:
            match_prefix = match.name[:-len(simple_filename)]
            if match_prefix.endswith(' - ') and match_prefix[:-3].isdigit():
                return match

        return None


    def __hash__(self) -> int:
        return hash(self.isrc)

    def __eq__(self, other) -> bool:
        if not isinstance(other, SpotifySong):
            return False

        return self.isrc == other.isrc

    def __dict__(self) -> dict[str, Any]:
        return {
            'added_at': self.added_at.isoformat(),
            'artists': self.artists,
            'title': self.title,
            'album_name': self.album_name,
            'album_image_url': self.album_image_url,
            'isrc': self.isrc,
            'year': self.year,
        }

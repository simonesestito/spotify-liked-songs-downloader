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

    def filename(self, extension: str | None = 'mp3') -> str:
        artists = ', '.join(self.normalized_artists)

        # Normalize the extension
        if extension and extension[0] != '.':
            extension = '.' + extension
        elif not extension:
            extension = ''

        return f'{self.normalized_title} - {artists}{extension}'

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

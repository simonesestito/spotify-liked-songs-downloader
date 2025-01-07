from dataclasses import dataclass

from src.spotify import SpotifySong


@dataclass
class YouTubeSong:
    id: str
    info: SpotifySong

    @property
    def url(self):
        return f'https://music.youtube.com/watch?v={self.id}'

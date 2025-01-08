import pathlib
import yt_dlp

from src.youtube import YouTubeSong


class YouTubeDownloader:
    def __init__(self, music_path: pathlib.Path):
        self.music_path = music_path

    def download(self, song: YouTubeSong, dest_dir: pathlib.Path | None = None) -> pathlib.Path:
        music_path = dest_dir or self.music_path
        song_file = music_path / song.info.filename(extension=None)

        with yt_dlp.YoutubeDL({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'm4a',
                }],
                'outtmpl': str(song_file.resolve()),
                'noplaylist': True,
                'retries': 3,
                'no_warnings': True,
                'quiet': True,
                'verbose': False,
                'noprogress': True,
            }) as downloader:
                downloader.download([song.url])

        return song_file.with_suffix('.m4a')

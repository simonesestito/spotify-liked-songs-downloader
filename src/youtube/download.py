import pathlib
import yt_dlp

from src.youtube.youtube_song import YouTubeSong


class YouTubeDownloader:
    def __init__(self, music_path: pathlib.Path):
        self.music_path = music_path

    def download(self, song: YouTubeSong, dest_dir: pathlib.Path | None = None) -> pathlib.Path:
        music_path = dest_dir or self.music_path
        song_file = music_path / song.info.filename(extension=None)

        downloader = yt_dlp.YoutubeDL({
            'format': 'bestaudio',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }],
            'outtmpl': str(song_file.resolve()),
            'noplaylist': True,
            'retries': 3,
            'no_warnings': True,
            'quiet': True,
            'verbose': False,
            'noprogress': True,
        })

        downloader.download([song.url])

        return song_file.with_suffix('.mp3')

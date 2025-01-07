import pathlib
import shutil
import tempfile

from src.metadata.tags_embedder import TagsEmbedder
from src.spotify import SpotifySong
from src.youtube.download import YouTubeDownloader
from src.youtube.search import YouTubeMusicSearch


class FullDownloader:
    def __init__(self, yt_search: YouTubeMusicSearch, yt_downloader: YouTubeDownloader, tagger: TagsEmbedder):
        self.yt_search = yt_search
        self.yt_downloader = yt_downloader
        self.tagger = tagger

    def download_song(self, song: SpotifySong):
        song_file = self.yt_downloader.music_path / song.filename()
        if song_file.exists():
            # Just update metadata
            self.tagger.embed_tags(song, song_file)
            return

        # Search on YouTube Music
        search_result = self.yt_search.search(song)
        if search_result is None:
            print(f'WARN: unable to find song on YouTube for {song.title}', flush=True)
            return

        with tempfile.TemporaryDirectory(prefix='spotify_download__') as temp_dir_name:
            temp_dir = pathlib.Path(temp_dir_name)

            # Download it
            temp_song_file = self.yt_downloader.download(search_result, dest_dir=temp_dir)

            # Embed the metadata
            self.tagger.embed_tags(song, temp_song_file)

            # Now that the job is completely finished, we can move the temp file to the actual directory
            shutil.move(temp_song_file, song_file)

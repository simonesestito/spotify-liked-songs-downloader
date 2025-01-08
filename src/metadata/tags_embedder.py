import os
import pathlib

import music_tag

from .image_downloader import ImageDownloader
from ..lyrics import LyricsAPI
from ..spotify import SpotifySong


class TagsEmbedder:
    def __init__(self, image_downloader: ImageDownloader, lyrics_api: LyricsAPI | None):
        self.image_downloader = image_downloader
        self.lyrics_api = lyrics_api

    def embed_tags(self, spotify_info: SpotifySong, file: pathlib.Path):
        # Load the file
        file_info = music_tag.load_file(str(file))

        artists = ', '.join(spotify_info.artists)

        file_info['artist'] = artists
        file_info['tracktitle'] = spotify_info.title
        file_info['album'] = spotify_info.album_name
        file_info['isrc'] = spotify_info.isrc
        file_info['year'] = spotify_info.year

        # Then, download the album cover image
        existing_artwork = None
        try:
            existing_artwork = file_info['artwork']
        except KeyError:
            pass

        # Skip the download if no URL is available, or an existing artwork is already included
        if spotify_info.album_image_url and existing_artwork is None:
            album_cover_bytes = self.image_downloader.download_image(spotify_info.album_image_url)
            file_info['artwork'] = album_cover_bytes
            file_info['artwork'].value.mime = 'image/jpeg'

        # Look for the lyrics, if not already included
        if self.lyrics_api and not file_info['lyrics']:
            lyrics = self.lyrics_api.search_song(spotify_info)
            file_info['lyrics'] = lyrics

        file_info.save()

        # Change the last modified date to the date of the like on Spotify
        last_edit_time = spotify_info.added_at.timestamp()
        os.utime(str(file), (last_edit_time, last_edit_time))

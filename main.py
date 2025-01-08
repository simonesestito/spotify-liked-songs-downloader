import argparse
import multiprocessing
import pathlib
import time
from queue import Empty
from typing import Any

from tqdm import tqdm

from src.downloader import FullDownloader
from src.metadata.image_downloader import ImageDownloader
from src.metadata.tags_embedder import TagsEmbedder
from src.spotify import SpotifyAPI, SpotifySong
from src.youtube.download import YouTubeDownloader
from src.youtube.search import YouTubeMusicSearch


def read_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Spotify Downloader')

    parser.add_argument(
        '--data-path', '-d',
        type=pathlib.Path,
        default=pathlib.Path('data/'),
        help='Folder where to store the fetched data (default: data/)'
    )

    parser.add_argument(
        '--music-path', '-m',
        type=pathlib.Path,
        default=pathlib.Path('data/music/'),
        help='Folder where to store the downloaded music (default: data/music/)'
    )

    parser.add_argument(
        '--refresh-liked-songs', '-r',
        action='store_true',
        help='Refresh the liked songs from the Spotify API (default: False)'
    )

    parser.add_argument(
        '--threads', '-t',
        type=int,
        default=6,
        help='Number of threads (default: 6)',
    )

    parser.add_argument(
        '--sort-liked-songs', '-S',
        action='store_true',
        help='Sort liked songs, adding a numbered prefix to allow sorting by their filename (default: False)'
    )

    parser.add_argument(
        '--cli-login', '-L',
        action='store_true',
        help='Login using a link, and not directly opening a browser. Useful in SSH'
    )

    return parser.parse_args()


def main():
    args = read_arguments()

    data_path = pathlib.Path(args.data_path)
    music_path = pathlib.Path(args.music_path)
    refresh_liked_songs = args.refresh_liked_songs
    threads_count = args.threads
    sort_liked_songs = args.sort_liked_songs
    cli_login = args.cli_login

    data_path.mkdir(parents=True, exist_ok=True)
    music_path.mkdir(parents=True, exist_ok=True)

    api = SpotifyAPI(data_path, cli_login)
    if refresh_liked_songs:
        print('Refreshing liked songs...')
        api.refresh_saved_liked_songs()
    else:
        print('Using cached liked songs')

    songs = api.load_cached_liked_songs()
    songs.sort(key=lambda s: s.added_at, reverse=True)

    songs_to_download = list(enumerate(songs))
    songs_queue = multiprocessing.Queue(maxsize=len(songs_to_download))
    for i, song in songs_to_download:
        songs_queue.put_nowait((i, song.__dict__()))

    threads = []
    completed_count = multiprocessing.Value('I', 0)  # 16 bits
    for _ in range(threads_count):
        thread = multiprocessing.Process(
            target=downloader_thread,
            args=(completed_count, music_path, songs_queue, sort_liked_songs),
        )
        thread.start()
        threads.append(thread)

    # Show the completion status
    is_running = multiprocessing.Value('b', 1)  # byte bool flag
    status_thread = multiprocessing.Process(
        target=print_threads_status,
        args=(completed_count, len(songs_to_download), is_running,),
    )
    status_thread.start()

    # Now, wait for them to finish
    for thread in threads:
        thread.join()

    print('Shutting down...', flush=True)
    songs_queue.close()
    is_running.value = 0
    status_thread.join()
    songs_queue.cancel_join_thread()  # We don't care about the queued songs anymore


def downloader_thread(completed_count: multiprocessing.Value, music_path: pathlib.Path,
                      songs: 'multiprocessing.Queue[tuple[int, dict[str, Any]]]',
                      sort_liked_songs: bool) -> None:
    downloader = FullDownloader(
        yt_search=YouTubeMusicSearch(),
        yt_downloader=YouTubeDownloader(music_path),
        tagger=TagsEmbedder(
            image_downloader=ImageDownloader(),
        ),
    )

    while not songs.empty():
        try:
            i, song_dict = songs.get(block=True, timeout=5)
        except Empty:
            return

        song = SpotifySong.from_dict(song_dict)
        downloader.download_song(song, i, sort_liked_songs)

        # Signal the successful completion
        with completed_count.get_lock():
            completed_count.value += 1


def print_threads_status(completed_count: multiprocessing.Value, songs_count: int, is_running: multiprocessing.Value):
    time.sleep(2)

    old_completed_count = completed_count.value
    progress_bar = tqdm(total=songs_count, initial=old_completed_count)

    while is_running.value:
        time.sleep(1)
        new_completed_count = completed_count.value
        diff_count = new_completed_count - old_completed_count
        progress_bar.update(diff_count)
        old_completed_count = new_completed_count

    progress_bar.close()
    print('Done.', flush=True)


if __name__ == '__main__':
    main()

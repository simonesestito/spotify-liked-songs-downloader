# Spotify Downloader

Easy, fast, effective.

Download all your liked songs, offline, from YouTube Music.

## Usage
- clone the repository
- install the *Poetry* project, by running `poetry install --no-root` ([Poetry](https://python-poetry.org/docs/main/#installing-with-the-official-installer) required)
- create a [Spotify Developer Project](https://developer.spotify.com/dashboard)
- export the following variables:
  - `SPOTIPY_CLIENT_ID` = the client ID of the Spotify project
  - `SPOTIPY_CLIENT_SECRET` = the client secret of the Spotify project
- run `python main.py` (the default arguments are okay)
- wait, wait and wait, until you'll find all your downloaded songs in the `./data/music` folder,
  ready to be played using your favourite MP3 player

### Example script
Take a look at [example-run-spotify.sh](example-run-spotify.sh).

### New songs added?

In case time goes by, and you like new songs on Spotify,
simply run the program again with the `-r` flag,
and they will be added to your folder.

```shell
python main.py -r
```

## Embed lyrics
To embed lyrics, pass the `--embed-lyrics` flag to the Python program.

### Optional arguments
You can list the available arguments by running `python main.py --help`.

Here's a snapshot of the available options:
```
-h, --help            show this help message and exit
--data-path DATA_PATH, -d DATA_PATH
                      Folder where to store the fetched data (default: data/)
--music-path MUSIC_PATH, -m MUSIC_PATH
                      Folder where to store the downloaded music (default: data/music/)
--refresh-liked-songs, -r
                      Refresh the liked songs from the Spotify API (default: False)
--threads THREADS, -t THREADS
                      Number of threads (default: 6)
--sort-liked-songs, -S
                      Sort liked songs, adding a numbered prefix to allow sorting by their filename (default: False)
--cli-login, -L       Login using a link, and not directly opening a browser. Useful in SSH
--embed-lyrics, -l    Embed Lyrics in the MP3 file (default: False)
```


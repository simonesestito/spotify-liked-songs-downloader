import requests


class LRCLibLyrics:
    def __init__(self, base_url: str | None = None, headers: dict[str, str] | None = None):
        self.base_url = base_url or "https://lrclib.net/api"
        self.headers = {
            "Accept": "application/json",
            "Lrclib-Client": "github.com/simonesestito/spotify-ytmusic-download",
            **(headers or {})
        }


    def query_lyrics(self, track_name: str, artist_name: str) -> str | None:
        exact_match = self._get_exact_match(track_name, artist_name)
        if exact_match is not None:
            return exact_match

        return self._search_best_match(track_name, artist_name)


    def _get_exact_match(self, track_name: str, artist_name: str) -> str | None:
        params = {
            "track_name": track_name,
            "artist_name": artist_name,
        }

        # Make the GET request
        response = requests.get(f'{self.base_url}/get', headers=self.headers, params=params)
        return LRCLibLyrics._parse_response(response)


    def _search_best_match(self, track_name: str, artist_name: str) -> str | None:
        params = {
            "track_name": track_name,
            "artist_name": artist_name,
        }

        response = requests.get(f'{self.base_url}/search', headers=self.headers, params=params)
        print('Best match for', track_name, artist_name, end='', flush=True)
        return LRCLibLyrics._parse_response(response)


    @staticmethod
    def _parse_response(response) -> str | None:
        # Handle not-found
        if response.status_code == 404:
            return None

        response.raise_for_status()

        data = response.json()

        if isinstance(data, list):
            data = next((entry for entry in data if entry['syncedLyrics'] or entry['plainLyrics']), None)
            if data is None:
                return None

            print(' is', data['trackName'], data['artistName'], flush=True)

        if 'instrumental' in data and data['instrumental']:
            return ''  # Not None, but an empty lyrics

        if 'syncedLyrics' in data and data['syncedLyrics'] is not None:
            return data['syncedLyrics']

        if 'plainLyrics' in data:
            return data['plainLyrics']

        return None

import urllib.request


class ImageDownloader:
    # noinspection PyMethodMayBeStatic
    def download_image(self, url: str) -> bytes:
        with urllib.request.urlopen(url) as response:
            return response.read()

import re
import unicodedata


def normalize_string(unicode_string: str, non_ascii_placeholder: str = '') -> str:
    # Replace special dashes
    unicode_string = unicode_string.replace('\u2013', '-')

    # Convert it to ASCII
    ascii_string = unicodedata.normalize('NFKD', unicode_string).encode('ascii', 'ignore').decode('ascii')

    # Replace letters different from A-Z, a-z, 0-9, - with _
    normalized_string = re.sub(r'[^A-Za-z0-9\-\s]', non_ascii_placeholder, ascii_string)

    return normalized_string

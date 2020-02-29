import re
import unicodedata

_NON_WORD_RE = re.compile(r'\W')


# See https://stackoverflow.com/a/518232
def strip_accents(s: str) -> str:
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')


def slugify(s: str) -> str:
    return _NON_WORD_RE.sub('-', strip_accents(s).lower())

from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass
class ParsedURL:
    url: str

    def __post_init__(self):
        parsed = urlparse(self.url)
        self.username = parsed.username
        self.password = parsed.password
        self.hostname = parsed.hostname
        self.port = parsed.port

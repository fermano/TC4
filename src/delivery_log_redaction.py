from urllib.parse import urlsplit, urlunsplit


def redact_delivery_url(url):
    parts = urlsplit(url)
    return urlunsplit((parts.scheme, parts.netloc, parts.path, "", parts.fragment))

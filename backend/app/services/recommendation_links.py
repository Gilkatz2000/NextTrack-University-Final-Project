from urllib.parse import quote_plus


def build_spotify_search_url(track, artist):
    query = quote_plus(f"{track} {artist}")
    return f"https://open.spotify.com/search/{query}"


def build_youtube_search_url(track, artist):
    query = quote_plus(f"{track} {artist} official audio")
    return f"https://www.youtube.com/results?search_query={query}"
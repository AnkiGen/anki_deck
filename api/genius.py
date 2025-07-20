import os
from requests.exceptions import Timeout, HTTPError
from dotenv import load_dotenv
from lyricsgenius import Genius
from time import sleep

load_dotenv()
access_token = os.getenv("GENIUS_ACCESS_TOKEN")
genius = Genius(access_token)
genius._session.proxies = {
    'http': os.getenv('HTTP_PROXY'),
    'https': os.getenv('HTTPS_PROXY')
}
genius.remove_section_headers = True
genius.skip_non_songs = True
genius.excluded_terms = ["(Remix)", "(Live)"]

def get_genius_text(artist_name, song_title):
    #while True:
     #   try:
     #       song = genius.search_song(title=song_title, artist=artist_name)
     #       lyrics = song.lyrics
     #       if "Read More" in lyrics:
     #           lyrics = lyrics.split("Read More")[1].strip()
     #       lyrics = '\n'.join(lyrics.split('\n')[1:])
     #       return lyrics
     #   except Timeout:
     #       sleep(5)
     #   except HTTPError:
     #       sleep(5)
    song = genius.search_song(title=song_title, artist=artist_name)
    lyrics = song.lyrics
    if "Read More" in lyrics:
        lyrics = lyrics.split("Read More")[1].strip()
    lyrics = '\n'.join(lyrics.split('\n')[1:])
    return lyrics

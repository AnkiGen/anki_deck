import os
from dotenv import load_dotenv
from lyricsgenius import Genius

load_dotenv()
access_token = os.getenv("GENIUS_ACCESS_TOKEN")
genius = Genius(access_token)
genius.remove_section_headers = True
genius.skip_non_songs = False
genius.excluded_terms = ["(Remix)", "(Live)"]

def get_genius_text(artist_name, song_title):
    song = genius.search_song(title=song_title, artist=artist_name)
    return song.lyrics

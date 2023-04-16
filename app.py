import youtube as yt
import dbclient as db

client = db.create_client()
collection = client['music']['music']
artist = 'Taylor Swift'
song = 'All Of The Girls You Loved Before'
channel = 'Sing King'

def add_to_library(artist, song):
    results = yt.search(artist, song, channel)
    client.
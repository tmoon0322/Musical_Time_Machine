import requests
from bs4 import BeautifulSoup
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pprint


CLIENT_ID = os.environ["SPOTIPY_CLIENT_ID"]
CLIENT_SECRET = os.environ["SPOTIPY_CLIENT_SECRET"]
SPOTIPY_REDIRECT_URI = os.environ["SPOTIPY_REDIRECT_URI"]


search_date = input("Enter the date you would like to create the playlist for: (YYYY-MM-DD)\n")
URL = "https://www.billboard.com/charts/hot-100/" + search_date + "/"
response = requests.get(url=URL)
response.raise_for_status()
billboard_webpage = response.text

soup = BeautifulSoup(billboard_webpage, "html.parser")
song_tags = soup.select("li ul li h3")
songs = [title.getText(strip=True) for title in song_tags]
print(songs)
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        client_secret=CLIENT_SECRET,
        client_id=CLIENT_ID,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        show_dialog=True,
        cache_path="token.txt",
        username="Thomas Moon"
    )
)

user_id = sp.current_user()["id"]


year = search_date.split("-")[0]
song_uris = []

new_playlist = sp.user_playlist_create(
    user=user_id,
    name=f"{search_date} Billboard 100",
    public=False,
    description="At this point, I'm just tryna finish this project"
)
playlist_id = new_playlist["id"]

for song in songs:
    results = sp.search(q=f"track: {song} year: {year}", type="track", limit=5)
    try:
        uri = results["tracks"]["items"][0]["uri"]
    except IndexError:
        print(f"{song} is not on Spotify. Skipped")
    else:
        song_uris.append(uri)

sp.user_playlist_add_tracks(
    user=user_id,
    playlist_id=playlist_id,
    tracks=song_uris,
)







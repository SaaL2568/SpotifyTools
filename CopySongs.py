import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# === Credentials from .env ===
CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

SCOPE = 'playlist-read-private playlist-modify-private playlist-modify-public'

# === Playlist IDs ===
SOURCE_PLAYLIST_ID = '1UefW4rj0MSgFVl2ENLbd3'   # Playlist A (source, with custom order)
TARGET_PLAYLIST_ID = '3M0pOEUDWMcOfEoIMYWr9B'   # Playlist B (existing one you want to overwrite)

# === AUTH ===
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE,
    cache_path=os.path.expanduser("~/.spotipyoauthcache")
))

# === Step 1: Fetch all tracks from Playlist A in custom order ===
tracks = []
offset = 0
while True:
    response = sp.playlist_items(
        SOURCE_PLAYLIST_ID,
        offset=offset,
        fields='items.track.uri,total,next',
        additional_types=['track']
    )
    items = response['items']
    if not items:
        break
    tracks.extend([item['track']['uri'] for item in items if item['track']])
    offset += len(items)

print(f"Found {len(tracks)} tracks in Playlist A")
tracks.reverse()

# === Step 2: Clear existing tracks in Playlist B (optional safety step) ===
# If you want to wipe B first so it *only* has A’s order:
# sp.playlist_replace_items(TARGET_PLAYLIST_ID, [])  # empty Playlist B
# print("Cleared existing tracks in Playlist B")

# === Step 3: Add tracks one by one to Playlist B ===
for i, track_uri in enumerate(tracks):
    sp.playlist_add_items(TARGET_PLAYLIST_ID, [track_uri])
    print(f"Added {i+1}/{len(tracks)}: {track_uri}")
    time.sleep(0.3)  # ensures unique "added at" timestamps

print("✅ Done! Open Playlist B and sort by 'Recently Added' — it will match Playlist A's custom order")

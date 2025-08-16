import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Your credentials and settings
CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

CACHE_PATH = os.path.expanduser("~/.spotipyoauthcache")  # Or any path you have write access to

SCOPE = 'playlist-read-private playlist-modify-private playlist-modify-public'



SOURCE_PLAYLIST_ID = 'playlist_id'  # Playlist A

# Your target playlist name
TARGET_PLAYLIST_NAME = 'Copy of Playlist A (Preserving Order)'

# === AUTH ===
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE,
    cache_path=os.path.expanduser("~/.spotipyoauthcache")
))

# === Step 1: Get current user ID
user_id = sp.current_user()['id']

# === Step 2: Fetch all tracks from Playlist A in custom order
tracks = []
offset = 0
while True:
    response = sp.playlist_items(SOURCE_PLAYLIST_ID,
                                 offset=offset,
                                 fields='items.track.uri,total,next',
                                 additional_types=['track'])
    items = response['items']
    if not items:
        break
    tracks.extend([item['track']['uri'] for item in items if item['track']])
    offset += len(items)

print(f"Found {len(tracks)} tracks in Playlist A")

new_playlist_id = '3M0pOEUDWMcOfEoIMYWr9B'
print(f"Created new playlist: {TARGET_PLAYLIST_NAME}")

# === Step 5: Add tracks one by one to preserve order in 'Recently Added'
for i, track_uri in enumerate(tracks):
    sp.playlist_add_items(new_playlist_id, [track_uri])
    print(f"Added {i+1}/{len(tracks)}: {track_uri}")
    time.sleep(0.3)  # Optional: ensures unique "added at" timestamps

print("✅ Done! Open the new playlist and sort by 'Recently Added' — it will match Playlist A's cu")
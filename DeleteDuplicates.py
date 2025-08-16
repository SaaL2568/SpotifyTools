import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# === Load environment variables ===
load_dotenv()

CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI", "http://localhost:8888/callback/")
SCOPE = "playlist-read-private playlist-modify-private playlist-modify-public"

# === Playlists ===
PLAYLIST_A_ID = "3M0pOEUDWMcOfEoIMYWr9B"  # The playlist you want to clean
PLAYLIST_B_ID = "1UefW4rj0MSgFVl2ENLbd3"  # The reference playlist

# === Auth ===
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE,
    cache_path=os.path.expanduser("~/.spotipyoauthcache")
))

# === Helper to fetch all tracks from a playlist ===
def get_all_tracks(playlist_id):
    tracks = []
    offset = 0
    while True:
        response = sp.playlist_items(
            playlist_id,
            offset=offset,
            fields="items.track.uri,total,next",
            additional_types=["track"]
        )
        items = response["items"]
        if not items:
            break
        tracks.extend([item["track"]["uri"] for item in items if item["track"]])
        offset += len(items)
    return tracks

# === Step 1: Fetch tracks ===
tracks_a = get_all_tracks(PLAYLIST_A_ID)
tracks_b = set(get_all_tracks(PLAYLIST_B_ID))

print(f"Playlist A has {len(tracks_a)} tracks")
print(f"Playlist B has {len(tracks_b)} tracks")

# === Step 2: Find duplicates ===
duplicates = [uri for uri in tracks_a if uri in tracks_b]

print(f"Found {len(duplicates)} duplicates to remove")

# === Step 3: Remove duplicates from Playlist A ===
for i in range(0, len(duplicates), 100):  # Spotify API limit = 100 per request
    sp.playlist_remove_all_occurrences_of_items(PLAYLIST_A_ID, duplicates[i:i+100])

print("✅ Done! Duplicates removed from Playlist A.")

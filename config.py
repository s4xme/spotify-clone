# Auralis configuration. Keep credentials in environment variables, never in Git.
import os

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "")
REDIRECT_URI = os.getenv("REDIRECT_URI", "http://127.0.0.1:5000/callback")
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "5000"))
DEBUG = os.getenv("DEBUG", "true").lower() in {"1", "true", "yes"}
SECRET_KEY = os.getenv("SECRET_KEY", "change-me-to-a-long-random-string")

# Permissions the app asks for
SCOPES = (
    "streaming user-read-email user-read-private "
    "user-read-playback-state user-modify-playback-state "
    "user-read-recently-played user-top-read "
    "playlist-read-private playlist-read-collaborative "
    "playlist-modify-public playlist-modify-private "
    "user-library-read user-library-modify"
)

# Auralis

Auralis is a sleek, responsive Spotify companion player built with Flask and the Spotify Web Playback SDK. Connect your Spotify account to search your music, browse your library, manage playlists, and control playback from one focused interface.

> Auralis is an independent project and is not affiliated with Spotify. Spotify Premium is required for playback through the Web Playback SDK. Spotify API access and development-mode user restrictions apply.

## Features

- Spotify sign-in using the OAuth authorization-code flow
- Search tracks and albums, and browse your playlists and liked songs
- Play, pause, skip, seek, shuffle, and repeat
- Create and edit playlists, save tracks, and add songs to the queue
- Responsive desktop and mobile layouts

## Requirements

- Python 3.10 or newer
- A Spotify account; Spotify Premium is needed for playback
- A Spotify developer app with the Web API and Web Playback SDK enabled

## Run locally

1. Clone the repository and change into its directory:

   ```bash
   git clone https://github.com/YOUR-USERNAME/auralis.git
   cd auralis
   ```

2. Create and activate a virtual environment:

   **Windows PowerShell**

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   **macOS / Linux**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Create a Spotify app in the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard). Add this Redirect URI to the app settings:

   ```text
   http://127.0.0.1:5000/callback
   ```

5. Set the Spotify app credentials and a strong Flask session key as environment variables.

   **Windows PowerShell**

   ```powershell
   $env:SPOTIFY_CLIENT_ID = "your-client-id"
   $env:SPOTIFY_CLIENT_SECRET = "your-client-secret"
   $env:SECRET_KEY = "replace-with-a-long-random-secret"
   ```

   **macOS / Linux**

   ```bash
   export SPOTIFY_CLIENT_ID="your-client-id"
   export SPOTIFY_CLIENT_SECRET="your-client-secret"
   export SECRET_KEY="replace-with-a-long-random-secret"
   ```

   These variables apply to the current terminal session. Never commit real credentials or production secrets to Git.

6. Start the app and open the exact local address below:

   ```bash
   python app.py
   ```

   Visit <http://127.0.0.1:5000>. Use `127.0.0.1`, not `localhost`, so the browser origin matches the registered Spotify redirect URI.

If your Spotify app is in development mode, add each tester to its allowed users in the Spotify dashboard. The app requests permissions for playback, profile, search, library, and playlist features.

## Configuration

| Variable | Purpose | Default |
| --- | --- | --- |
| `SPOTIFY_CLIENT_ID` | Spotify app client ID | Empty (required) |
| `SPOTIFY_CLIENT_SECRET` | Spotify app client secret | Empty (required) |
| `SECRET_KEY` | Signs Flask session cookies | Insecure local-development value; replace it |
| `REDIRECT_URI` | OAuth callback URL | `http://127.0.0.1:5000/callback` |
| `HOST` | Development server bind address | `127.0.0.1` |
| `PORT` | Development server port | `5000` |
| `DEBUG` | Flask debug mode | `true` |

The built-in Flask server and default settings are for local development. Before hosting Auralis publicly, configure HTTPS and Spotify's approved redirect URI, use a production WSGI server, set `DEBUG=false`, and use a unique secret key stored in your hosting provider's secret manager.

## Tech stack

- Python, Flask, Requests
- Vanilla HTML, CSS, and JavaScript
- Spotify Web API and Spotify Web Playback SDK

## License

No license has been selected yet. Unless a license is added, the default copyright rules apply and others do not automatically have permission to reuse, modify, or distribute this code. Add a `LICENSE` file when you decide how you want the project to be shared.

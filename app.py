import os
import secrets
import sys
import time
from urllib.parse import urlencode

import requests
from flask import (Flask, Response, jsonify, redirect, request, send_from_directory, session)

import config

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, static_folder=os.path.join(BASE_DIR, "static"))
app.secret_key = config.SECRET_KEY

AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
API_URL = "https://api.spotify.com/v1"


def _save_tokens(data):
    session["access_token"] = data["access_token"]
    session["expires_at"] = time.time() + data["expires_in"]
    if data.get("refresh_token"):
        session["refresh_token"] = data["refresh_token"]


def _token_request(form):
    # The client secret stays on the server and is never sent to the browser.
    return requests.post(TOKEN_URL, data=form, auth=(config.CLIENT_ID, config.CLIENT_SECRET), timeout=15)


def get_token():
    """Return a valid access token, refreshing it if needed. None if logged out."""
    if "access_token" not in session:
        return None
    if time.time() > session.get("expires_at", 0) - 60:
        refresh = session.get("refresh_token")
        if not refresh:
            session.clear()
            return None
        r = _token_request({"grant_type": "refresh_token", "refresh_token": refresh})
        if not r.ok:
            session.clear()
            return None
        _save_tokens(r.json())
    return session["access_token"]


@app.route("/")
def index():
    # Works whether index.html is in the "static" folder or right next to app.py
    for folder in (os.path.join(BASE_DIR, "static"), BASE_DIR):
        if os.path.isfile(os.path.join(folder, "index.html")):
            return send_from_directory(folder, "index.html")
    return ("index.html not found. Put it in a folder named 'static' next to app.py "
            f"(looked in {BASE_DIR}).", 404)


@app.route("/login")
def login():
    state = secrets.token_urlsafe(16)
    session["oauth_state"] = state
    params = {
        "response_type": "code",
        "client_id": config.CLIENT_ID,
        "scope": config.SCOPES,
        "redirect_uri": config.REDIRECT_URI,
        "state": state,
    }
    return redirect(f"{AUTH_URL}?{urlencode(params)}")


@app.route("/callback")
def callback():
    if request.args.get("error"):
        return redirect("/?error=" + request.args["error"])
    if request.args.get("state") != session.pop("oauth_state", None):
        return redirect("/?error=state_mismatch")
    r = _token_request({
        "grant_type": "authorization_code",
        "code": request.args.get("code", ""),
        "redirect_uri": config.REDIRECT_URI,
    })
    if not r.ok:
        return redirect("/?error=token_exchange_failed")
    _save_tokens(r.json())
    session.permanent = True
    return redirect("/")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/api/token")
def token():
    """Used by the Spotify Web Playback SDK in the browser."""
    t = get_token()
    if not t:
        return jsonify(error="not_logged_in"), 401
    return jsonify(access_token=t)


@app.route("/api/spotify/<path:path>", methods=["GET", "PUT", "POST", "DELETE"])
def proxy(path):
    """Forwards requests to the Spotify Web API using the logged-in user's token."""
    t = get_token()
    if not t:
        return jsonify(error="not_logged_in"), 401
    r = requests.request(
        request.method, f"{API_URL}/{path}",
        params=request.args, json=request.get_json(silent=True),
        headers={"Authorization": f"Bearer {t}"}, timeout=20,
    )
    return Response(r.content, r.status_code, content_type=r.headers.get("Content-Type", "application/json"))


if __name__ == "__main__":
    if not config.CLIENT_ID or not config.CLIENT_SECRET:
        sys.exit("Set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET before starting Auralis.")
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)

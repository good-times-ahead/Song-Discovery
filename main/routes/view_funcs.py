# storing the functions to be used alongside/in the views of the main views file
import spotipy
from functools import wraps
from flask import flash, session, redirect, url_for
from os import getenv

# setup env & scope to define access to the spotify web api
client_id = getenv("CLIENT_ID")
client_secret = getenv("CLIENT_SECRET")
redirect_uri = getenv("REDIRECT_URI")

scope = "user-library-read user-top-read user-read-recently-played user-library-modify"


def init():
    """
    Initialize the Spotify API object here
    """
    sp = spotipy.oauth2.SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scope,
        show_dialog=True,
    )

    return sp


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        # if the user hasn't logged in and is accessing the pages directly or through some work-around
        if not session["token_info"]:

            flash("Not logged in.")

            return redirect(url_for("main.index"))

        # refresh the token if it has expired
        if spotipy.SpotifyOAuth.is_token_expired(session["token_info"]):

            refresh_token = session["token_info"]["refresh_token"]

            get_new_token = init().refresh_access_token(refresh_token)

            session["token_info"] = get_new_token

            flash("Your token has been renewed.")

        return f(*args, **kwargs)

    return decorated_function

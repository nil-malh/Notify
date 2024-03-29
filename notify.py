import os

from time import sleep
from datetime import datetime
import base64
import requests

# Spotipy import
import spotipy

# Instagrapi Imports
from instagrapi import Client
from dotenv import load_dotenv


def print_welcome_message():
    logo = '''⠀⠀⠀⠀⠀⠀⠀⢀⣠⣤⣤⣶⣶⣶⣶⣤⣤⣄⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢀⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⡀⠀⠀⠀⠀
⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠀⠀
⠀⢀⣾⣿⡿⠿⠛⠛⠛⠉⠉⠉⠉⠛⠛⠛⠿⠿⣿⣿⣿⣿⣿⣷⡀⠀
⠀⣾⣿⣿⣇⠀⣀⣀⣠⣤⣤⣤⣤⣤⣀⣀⠀⠀⠀⠈⠙⠻⣿⣿⣷⠀
⢠⣿⣿⣿⣿⡿⠿⠟⠛⠛⠛⠛⠛⠛⠻⠿⢿⣿⣶⣤⣀⣠⣿⣿⣿⡄
⢸⣿⣿⣿⣿⣇⣀⣀⣤⣤⣤⣤⣤⣄⣀⣀⠀⠀⠉⠛⢿⣿⣿⣿⣿⡇
⠘⣿⣿⣿⣿⣿⠿⠿⠛⠛⠛⠛⠛⠛⠿⠿⣿⣶⣦⣤⣾⣿⣿⣿⣿⠃      █▄░█ █▀█ ▀█▀ █ █▀▀ █▄█                                          
 ⢿⣿⣿⣿⣿⣤⣤⣤⣤⣶⣶⣦⣤⣤⣄⡀⠈⠙⣿⣿⣿⣿⣿⡿⠀      █░▀█ █▄█ ░█░ █ █▀░ ░█░
⠀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣾⣿⣿⣿⣿⡿⠁⠀
⠀⠀⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠀⠀⠀
⠀⠀⠀⠀⠈⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠈⠙⠛⠛⠿⠿⠿⠿⠛⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀'''

    print(logo)


def debug(message):
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"[{timestamp}] : {message}")


def setup_env_file():
    if not os.path.isfile(".env"):
        client_id = input("Please enter your Spotify client ID: ")
        client_secret = input("Please enter your Spotify client secret: ")
        print(f'In order to get your refresh token , you can visit this link : https://spotify-refresh-token-generator.netlify.app/')
        refresh_token = input("Please enter your Spotify refresh token: ")
        bot_refresh_rate = input("Please enter the bot refresh rate (in seconds): ")
        note_prefix = input("Please enter the desired prefix that will be displayed before the song name and artist")
        separator = input("Please enter the separator between the song name and the artist")
        ig_username = input("Please enter your Instagram username: ")
        ig_password = input("Please enter your Instagram password: ")

        if not bot_refresh_rate:
            debug("No specified refresh rate was specified. Defaulting to 180s")
            bot_refresh_rate = "180"

        with open(".env", "w") as env_file:
            env_file.write(f"SPOTIPY_CLIENT_ID={client_id}\n")
            env_file.write(f"SPOTIPY_CLIENT_SECRET={client_secret}\n")
            env_file.write(f"SPOTIPY_REFRESH_TOKEN={refresh_token}\n")
            env_file.write(f"BOT_REFRESH_RATE={bot_refresh_rate}\n")
            env_file.write(f'SONG_SEPARATOR={separator}')
            env_file.write(f"IG_USERNAME={ig_username}\n")
            env_file.write(f"IG_PASSWORD={ig_password}\n")
            env_file.write(f"IG_NOTE_PREFIX={note_prefix}\n")


print_welcome_message()
setup_env_file()
load_dotenv()

debug("Loading credentials from .env file ...")
load_dotenv()
debug("Credentials are loaded !")

# Instagram credentials and config file
IG_USERNAME = os.getenv("IG_USERNAME")
IG_PASSWORD = os.getenv("IG_PASSWORD")
IG_NOTE_PREFIX = os.getenv("IG_NOTE_PREFIX")
IG_CREDENTIAL_PATH = './ig_settings.json'

SLEEP_TIME = os.getenv("BOT_REFRESH_RATE")  # in seconds
SONG_SEPARATOR = os.getenv("SONG_SEPARATOR")
# Spotify credentials
SPOTIFY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIFY_REFRESH_TOKEN = os.getenv("SPOTIPY_REFRESH_TOKEN")

if not all([SPOTIFY_CLIENT_SECRET, SPOTIFY_CLIENT_ID, SPOTIFY_REFRESH_TOKEN]):
    raise Exception("Can't find Spotify credentials in the .env file")
if not SONG_SEPARATOR:
    SONG_SEPARATOR = "-"

def get_access_token(client_id, client_secret, refresh_token):
    debug("Getting an access token from Spotify API ...")
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }
    auth = f"{client_id}:{client_secret}"
    auth = auth.encode("utf-8")
    auth = base64.b64encode(auth).decode("utf-8")
    response = requests.post("https://accounts.spotify.com/api/token", data=data,
                             headers={
                                 "Authorization": f"Basic {auth}",
                             })

    if response.status_code != 200:
        raise Exception(f"Request failed with status code {response.status_code}: {response.text}")
    response_data = response.json()
    access_token = response_data["access_token"]
    debug("Access token has been retrieved from Spotify API !")
    return access_token


access_token = get_access_token(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REFRESH_TOKEN)
sp = spotipy.Spotify(auth=access_token)


class Bot:
    _cl = None

    def __init__(self):
        self._cl = Client()

        if not all([IG_USERNAME, IG_PASSWORD, IG_NOTE_PREFIX,IG_CREDENTIAL_PATH]):
            raise Exception("Can't find Instagram credentials in the .env file")
        if os.path.exists(IG_CREDENTIAL_PATH):
            self._cl.load_settings(IG_CREDENTIAL_PATH)
            debug(f'Connecting to Instagram as {IG_USERNAME}')
            self._cl.login(IG_USERNAME, IG_PASSWORD)
        else:
            TOTA = input("Please enter your 2FA code in order to connect to Instagram.")
            debug(f'Logging-in to Instagram as {IG_USERNAME} for the first time, with 2FA code : {TOTA}')
            self._cl.login(IG_USERNAME, IG_PASSWORD, verification_code=TOTA)
            debug(f'Logged-in to Instagram !')
            self._cl.dump_settings(IG_CREDENTIAL_PATH)
            debug('Instagram credentials has been saved !')

    def send_music_note(self, song_name, artist,separator):

        previous_note = None
        note_content = f"{IG_NOTE_PREFIX} {song_name} {separator} {artist}" if IG_NOTE_PREFIX else f"🎧  {song_name} {separator} {artist}"
        if note_content == previous_note and previous_note is not None:
            debug("The content of the note is the same as before, no need to send a new one")
        if len(note_content) < 60:
            self._cl.send_note(f"{IG_NOTE_PREFIX} : {song_name} {separator} {artist}" if IG_NOTE_PREFIX else f"🎧 : {song_name} {separator} {artist}", 0)
            previous_note = note_content

        else:
            print(f'The content of the note is too long. (note_content_len : {len(note_content)})')

    def update(self, spotify):

        current_track = spotify.current_playback()
        if current_track:
            song_name = current_track["item"]["name"]
            artist = current_track["item"]["artists"][0]["name"]
            note_content = f"{song_name} - {artist}"
            debug(note_content)
            debug("Sending note to Instagram API.")
            bot.send_music_note(song_name, artist,SONG_SEPARATOR)
            debug(f'Note should be set on {IG_USERNAME} account.')
        else:
            debug("Nothing is playing currently.")
        pass


if __name__ == '__main__':
    bot = Bot()
    trigger_fail = False
    while True:
        try:
            bot.update(sp)
            sleep(int(SLEEP_TIME))
        except spotipy.exceptions.SpotifyException as e:
            if e.http_status == 401:
                debug("Spotify token has expired, refreshing it...")
                access_token = get_access_token(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REFRESH_TOKEN)
                sp = spotipy.Spotify(auth=access_token)
                debug("Spotify token has been refreshed")
            else:
                raise e

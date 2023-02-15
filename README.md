
# Notify

Want to spice up your Notes on Instagram by displaying what you're currently playing on Spotify ? Here is Notify at your service ! 

## Installation

Install Notify from GitHub

### Download from GitHub
```bash
  git clone https://github.com/nil-malh/Notify.git
  cd Notify
```

### Download dependencies and run the project

```bash
  pip install -r requirements.txt && python notify.py
```
    
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file or input them when running the project for the first time.

`SPOTIPY_CLIENT_ID`:
*The client_id from your Spotify application*

`SPOTIPY_CLIENT_SECRET`:
*The client_secret from your Spotify application*

`SPOTIPY_REFRESH_TOKEN`:
*The refresh_token for the Authentication to the Spotify API*

`BOT_REFRESH_RATE`:
*The intervals between two notes sent to the Instagram API*

`IG_USERNAME`
*Your Instagram username*
`IG_PASSWORD`
*Your Instagram password*



## FAQ

#### How can I generate a refresh_token ? 

You can use this [project]("https://github.com/limhenry/spotify-refresh-token-generator") made by [@limhenry]("https://github.com/limhenry") to generate your refresh_token please be sure to check the scope `user-read-currently-playing` in order to authorize Notify to ask Spotify what you are currently listening to.

#### What value shoud I put in `BOT_REFRESH_RATE ?`

The value in BOT_REFRESH_RATE should at least 120 seconds to avoid triggering Instagram. You can put lower value if you like the risk but I am not reponsible for your account being restricted !

## Used dependencies

**Client:** 
* [Instagrapi]("https://github.com/adw0rd/instagrapi") (*Note implementation made by me !*)
* [Spotipy]("https://github.com/spotipy-dev/spotipy")



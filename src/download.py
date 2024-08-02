import json
import requests
from scraper.twitch import get_access_token, get_emotes


def get_twitch_emotes():
    try:
        access_token = get_access_token()
    except requests.exceptions.HTTPError as e:
        print(f"Failed to get access token: {e}")
    except KeyError as e:
        print("Access token not found in response")
        print("Response:", e)

    with open("response.json", "w") as f:
        json.dump(get_emotes(access_token), f)


def main():
    get_twitch_emotes()


if __name__ == "__main__":
    main()

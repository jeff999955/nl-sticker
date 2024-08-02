import json
import requests
from parser.twitch import parse_json
from scraper.twitch import get_access_token, get_emotes


def get_twitch_emotes():
    try:
        access_token = get_access_token()
    except requests.exceptions.HTTPError as e:
        print(f"Failed to get access token: {e}")
        return
    except KeyError as e:
        return

    try:
        emotes = get_emotes(access_token)
    except requests.exceptions.HTTPError as e:
        print(f"Failed to get emotes: {e}")
        return

    emotes = parse_json(emotes)
    for emote in emotes:
        print(emote)


def main():
    get_twitch_emotes()


if __name__ == "__main__":
    main()

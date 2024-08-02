import json
import os
import requests
import logging

BROADCASTER_ID = "29722828"

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def get_access_token():
    url = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": os.getenv("TWITCH_CLIENT_ID"),
        "client_secret": os.getenv("TWITCH_CLIENT_SECRET"),
        "grant_type": "client_credentials",
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    response = response.json()

    try:
        return response["access_token"]
    except KeyError as e:
        logger.error(f"Access token not found in response: {response}")
        raise e


def get_emotes(access_token):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Client-Id": os.getenv("TWITCH_CLIENT_ID"),
    }

    params = {
        "broadcaster_id": BROADCASTER_ID,
    }

    response = requests.get(
        "https://api.twitch.tv/helix/chat/emotes", params=params, headers=headers
    )
    response.raise_for_status()

    return response.json()


def main():
    try:
        access_token = get_access_token()
    except requests.exceptions.HTTPError as e:
        logger.error(f"Failed to get access token: {e}")
        return
    except KeyError:
        return

    try:
        emote_json = get_emotes(access_token)
    except requests.exceptions.HTTPError as e:
        logger.error(f"Failed to get emotes: {e}")
        return

    with open("response.json", "w") as f:
        json.dump(get_emotes(access_token), f)
        logger.info("Emotes data saved to response.json")


if __name__ == "__main__":
    main()

import json
import os
import requests

BROADCASTER_ID = "29722828"


def get_access_token():
    url = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": os.getenv("TWITCH_CLIENT_ID"),
        "client_secret": os.getenv("TWITCH_CLIENT_SECRET"),
        "grant_type": "client_credentials",
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    return response.json()["access_token"]


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
        print(f"Failed to get access token: {e}")
    except KeyError as e:
        print("Access token not found in response")
        print("Response:", e)

    with open("response.json", "w") as f:
        json.dump(get_emotes(access_token), f)


if __name__ == "__main__":
    main()

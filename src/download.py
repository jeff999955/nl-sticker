import logging
import requests
from parser.twitch import parse_json
from scraper.twitch import get_access_token, get_emotes

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def get_twitch_emotes():
    try:
        access_token = get_access_token()
    except requests.exceptions.HTTPError as e:
        logger.error(f"Failed to get access token: {e}")
        return
    except KeyError as e:
        return

    try:
        emotes = get_emotes(access_token)
    except requests.exceptions.HTTPError as e:
        logger.error(f"Failed to get emotes: {e}")
        return

    try:
        emotes = parse_json(emotes)
    except KeyError as e:
        logger.error(f"Failed to parse emotes: {e}")
        return

    for emote in emotes:
        url = emote["url"]
        response = requests.get(url)
        if response.status_code != 200:
            logger.error(f"Failed to download emote: {emote['name']}")
            continue

        with open(f"emotes/{emote['name']}.{emote['extension']}", "wb") as f:
            f.write(response.content)

        logger.info(f"Downloaded emote: {emote['name']}")


def main():
    get_twitch_emotes()


if __name__ == "__main__":
    main()

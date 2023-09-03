import argparse
import json
import os
import shutil
import tempfile
from typing import Literal

import requests
import tqdm


def main(args):
    os.makedirs(args.output_dir, exist_ok=True)

    with open(args.json_file, "r") as f:
        sticker_list = json.load(f)

    for sticker in tqdm.tqdm(sticker_list):
        src, name = sticker["src"], sticker["name"]

        if args.mode == "twitch":
            resolution = src.split("/")[-1]
            src = src.replace(resolution, "4.0")
        elif args.mode == "discord":
            pass
        img = requests.get(src).content

        # Check the file type with the first 4 bytes
        signature = img[:4]

        if signature == b"\x89PNG":
            extension = "png"
        elif signature == b"GIF8":
            extension = "gif"
        else:
            print(f"Unknown image signature for {name}.")
            continue

        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(img)  # Write the image to the file

        shutil.move(
            f.name, os.path.join(args.output_dir, f"{name}.{extension}")
        )  # Move the file to the correct path


def parse_cli_args():
    # Parse command line arguments with argparse
    parser = argparse.ArgumentParser(description="Download stickers with json list.")
    parser.add_argument(
        "-f",
        "--json-file",
        "--file",
        help="Path to the json file containing the list of stickers.",
        required=True,
    )
    parser.add_argument(
        "-d",
        "--output-dir",
        "--output",
        help="Path to the output directory.",
        required=True,
    )
    parser.add_argument(
        "-m",
        "--mode",
        help="Mode of the scraper. Either 'twitch' or 'discord'.",
        default="twitch",
        type=Literal["twitch", "discord"],
    )

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_cli_args()
    main(args)

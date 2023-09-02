import json
import os
import shutil
import tempfile

import requests
import tqdm

with open("twitch_sticker_list.json", "r") as f:
    sticker_list = json.load(f)

TWITCH_SAVE_PATH = "twitch_stickers"

for sticker in tqdm.tqdm(sticker_list):
    src, name = sticker["src"], sticker["name"]

    resolution = src.split("/")[-1]
    src = src.replace(resolution, "4.0")
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
        f.name, os.path.join(TWITCH_SAVE_PATH, f"{name}.{extension}")
    )  # Move the file to the correct path

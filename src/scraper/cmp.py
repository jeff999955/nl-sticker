import json

with open("/Users/nl/Documents/nl-sticker/src/scraper/internal_response.json") as f:
    internal = json.load(f)

internal = set(map(lambda x: x["name"], internal["data"]))
print(f"{len(internal)} internal emotes")

with open("/Users/nl/Documents/nl-sticker/src/scraper/response.json") as f:
    external_json = json.load(f)

external = set(
    map(
        lambda x: x["token"],
        external_json[0]["data"]["channel"]["localEmoteSets"][0]["emotes"],
    )
)

for s in external_json[0]["data"]["user"]["subscriptionProducts"]:
    external.update(
        map(
            lambda x: x["token"],
            s["emotes"],
        )
    )

print(f"{len(external)} external emotes")
print(f"{len(internal.intersection(external))} common emotes")

if internal > external:
    print(internal - external)
else:
    print(external - internal)

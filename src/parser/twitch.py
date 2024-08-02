from jinja2 import Template

TWITCH_FORMAT_TO_EXTENSION = {
    "static": "png",
    "animated": "gif",
}


def get_first(data, keys):
    for key in keys:
        if key in data:
            return data[key]

    return None


def parse_json(json_data):
    template = Template(json_data["template"])

    return_data = list(
        map(
            lambda x: {
                "id": x["id"],
                "name": x["name"],
                "format": x["format"][-1],
                "scale": x["scale"][-1],
                "theme_mode": x["theme_mode"][0],
            },
            json_data["data"],
        )
    )

    return_data = list(
        map(
            lambda x: {
                "name": x["name"],
                "extension": TWITCH_FORMAT_TO_EXTENSION[x["format"]],
                "url": template.render(x),
            },
            return_data,
        )
    )

    return return_data

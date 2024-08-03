const Handlebars = require("handlebars");
const { format } = require("logform");

TWITCH_FORMAT_TO_EXTENSION = {
  static: "png",
  animated: "gif",
};

const getFirst = (dict, keys) => {
  for (const key of keys) {
    if (dict[key]) {
      return dict[key];
    }
  }
  return null;
};

const parseJson = (json) => {
  template = Handlebars.compile(json["template"]);

  const emotes = json["data"]
    .map((emote) => ({
      id: emote.id,
      name: emote["name"],
      format: emote["format"].at(-1),
      scale: emote.scale.at(-1),
      theme_mode: emote.theme_mode.at(0),
    }))
    .map((emote) => ({
      name: emote.name,
      extension: TWITCH_FORMAT_TO_EXTENSION[emote.format],
      url: template(emote),
    }));

  return emotes;
};

module.exports = { parseJson };

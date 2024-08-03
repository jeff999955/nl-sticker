const { getAccessToken, getEmotes } = require("./scraper/twitch");
const { parseJson } = require("./parser/twitch");
const axios = require("axios");
const fs = require("fs");
const { v4 } = require("uuid");

const getTwitchEmotes = async (dirPath) => {
  const accessToken = await getAccessToken();
  let emotes = await getEmotes(accessToken);
  emotes = parseJson(emotes);
  await Promise.all(
    emotes.map(async ({ name, extension, url }) => {
      console.log(`${name}.${extension}: ${url}`);

      await axios.get(url, { responseType: "stream" }).then((res) => {
        res.data.pipe(
          fs.createWriteStream(`./${dirPath}/${name}.${extension}`)
        );
      });
    })
  );
};

(async () => {
  try {
    const tmpDirName = v4();
    fs.mkdirSync(`./${tmpDirName}`);
    await getTwitchEmotes(tmpDirName);
  } catch (error) {
    console.error(error);
  }
}).call(this);

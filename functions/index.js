const { onRequest } = require("firebase-functions/v2/https");
const logger = require("firebase-functions/logger");
const admin = require("firebase-admin");
const axios = require("axios");
const { getAccessToken, getEmotes } = require("./scraper/twitch");
const { parseJson } = require("./parser/twitch");

// Initialize the Firebase Admin SDK
admin.initializeApp();

exports.uploadTwitchEmotes = onRequest(async (req, res) => {
  try {
    const accessToken = await getAccessToken();
    let emotes = await getEmotes(accessToken);
    emotes = parseJson(emotes);

    const bucket = admin.storage().bucket();

    await Promise.all(
      emotes.map(async ({ name, extension, url }) => {
        logger.log(`${name}.${extension}: ${url}`);

        const response = await axios.get(url, { responseType: "stream" });
        const file = bucket.file(`${name}.${extension}`);
        const writeStream = file.createWriteStream();

        response.data.pipe(writeStream);

        return new Promise((resolve, reject) => {
          writeStream.on("finish", resolve);
          writeStream.on("error", reject);
        });
      })
    );

    res.status(200).send("Emotes uploaded successfully.");
  } catch (error) {
    logger.error("Error uploading emotes:", error);
    res.status(500).send("Error uploading emotes.");
  }
});

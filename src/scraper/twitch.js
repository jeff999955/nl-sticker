const axios = require("axios");
const logger = require("../utils/logger");

const BROADCASTER_ID = "29722828";

const getAccessToken = async () => {
  const url = "https://id.twitch.tv/oauth2/token";
  const params = {
    client_id: process.env.TWITCH_CLIENT_ID,
    client_secret: process.env.TWITCH_CLIENT_SECRET,
    grant_type: "client_credentials",
  };

  try {
    const response = await axios.post(url, null, { params });
    return response.data.access_token;
  } catch (error) {
    logger.error(
      `Failed to get access token: ${
        error.response ? error.response.data : error.message
      }`
    );
    throw error;
  }
};

const getEmotes = async (accessToken) => {
  const url = "https://api.twitch.tv/helix/chat/emotes";
  const headers = {
    "Authorization": `Bearer ${accessToken}`,
    "Client-Id": process.env.TWITCH_CLIENT_ID,
  };
  const params = {
    broadcaster_id: BROADCASTER_ID,
  };

  try {
    const response = await axios.get(url, { headers, params });
    return response.data;
  } catch (error) {
    logger.error(
      `Failed to get emotes: ${
        error.response ? error.response.data : error.message
      }`
    );
    throw error;
  }
};

module.exports = { getAccessToken, getEmotes };

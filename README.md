Future TJHSST classes may find use in this python script as an example of implementing both discord API and ion OAuth. 

# TJHSST Discord Verification Bot

This bot is designed to verify whether a user is part of the senior class at TJHSST using **Ion OAuth2**, the **Discord API**, and **Python**. It automatically assigns a "verified" role to verified users on Discord after successful authentication via Ion. This bot can be useful for managing TJ-specific access or privileges on Discord servers, and can be easily modified for other applications.

## Features
- Verifies senior status using Ion OAuth2.
- Assigns a "verified" role to verified users on the Discord server.
- Logs user commands for verification and interaction purposes.

## Requirements

- **Python 3.8+**
- [discord.py](https://pypi.org/project/discord.py/) library for Discord interaction
- [aiohttp](https://pypi.org/project/aiohttp/) library to handle the web server
- [requests-oauthlib](https://pypi.org/project/requests-oauthlib/) library for OAuth2 flow
- A Discord bot application with necessary intents enabled
- An Ion OAuth2 application for authentication

## Setup Instructions

### 1. Create a Discord Bot
1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Create a new application and navigate to the **Bot** tab.
3. Click **Add Bot** and copy the **Bot Token**.
4. Under **Privileged Gateway Intents**, enable the following:
   - **Server Members Intent** (to manage roles)
   - **Message Content Intent** (to process commands like `b.verify`).

### 2. Create an Ion OAuth2 Application
1. Go to the [Ion OAuth Applications](https://ion.tjhsst.edu/oauth/applications).
2. Register a new application with the following details:
   - **Client Type**: Confidential
   - **Authorization Grant Type**: Authorization Code
   - **Redirect URI**: Set to your testing or production URL (e.g., `http://localhost:5000/callback` or your public-facing URL if hosted).
3. Save the **Client ID** and **Client Secret** from the Ion application.

### 3. Clone This Repository
Clone the repository and navigate into the project directory:
`git clone https://github.com/bhkrayola/scavhuntverificationbot.git 
cd scavhuntverificationbot`

### 4. Install Python Dependencies
Install the required Python libraries using pip:
`pip install discord.py aiohttp requests-oauthlib`

### 5. Set Up Environment Variables
Create a .env file or set up environment variables in your operating system. Here's an example .env file:

`DISCORD_TOKEN=your_discord_bot_token
CLIENT_ID=your_ion_client_id
CLIENT_SECRET=your_ion_client_secret
REDIRECT_URI=http://localhost:5000/callback  # Or your public-facing URL
GUILD_ID=your_discord_guild_id
ROLE_ID=your_role_id`

### 6. Running the Bot Locally
To run the bot locally, simply use:
`python3 server.py`
If you're testing locally, you may need to expose your local server using ngrok to allow Ion OAuth to redirect back to your local machine. Run ngrok with:
`ngrok http 5000`
This will give you a public URL that you can use as your redirect URI during development.

### 7. Using the Bot
Once the bot is running, users can initiate the verification process in Discord by typing:
`b.verify`
The bot will send them a link to authenticate through Ion OAuth. Upon successful verification, the bot will assign the "verified" role to the user in Discord.

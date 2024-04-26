# Welcome!
 > ChatGPT Discord bot, easily integrate AI into your server!

## Table of contents
- [Welcome!](#welcome)
  - [Table of contents](#table-of-contents)
  - [Features](#features)
  - [Requirements](#requirements)
  - [Installation](#installation)
    - [Local](#local)
    - [Docker](#docker)
  - [Running the bot](#running-the-bot)
  - [Configuration](#configuration)
  - [License](#license)
  - [Contributing](#contributing)
  - [Thanks to xtekky for the wrapper!](#thanks-to-xtekky-for-the-wrapper)

## Features
- [x] Free API
- [x] Docker & Local Support
- [x] Private Sessions
- [x] Proxied/Proxyless Support
- [x] Saves Conversation Context

## Requirements
- Discord Bot
- Python 3.8 or higher

## Installation

### Local

1. Clone this repository to your local machine:
```bash
git clone https://github.com/kWAYTV/chatgpt-discord-bot.git
cd chatgpt-discord-bot
```

2. Install the required Python packages:
```bash
pip install -r requirements.txt
```
3. Create and fill a `.env` file in the project directory. See the [Configuration](#configuration) section below for more details.
4. Continue the installation by following the [Running the bot](#running-the-bot) section below.

### Docker

You can easily run the ChatGPT Discord bot using Docker. Here's how:

1. Clone this repository to your local machine:
```bash
git clone https://github.com/kWAYTV/chatgpt-discord-bot.git
cd chatgpt-discord-bot
```

2. Create a `docker-compose.yml` file in the project directory with the following content:
```yaml
version: '3.9'

services:
  chatgpt-discord-bot:
    image: harbor.kway.club/library/chatgpt-discord-bot:latest
    container_name: chatgpt-discord-bot
    volumes:
      - DATA_PATH:/app/data  # Mount the data directory if needed at runtime
    environment:
      - APP_LOGO=
      - APP_URL=
      - APP_NAME=
      - APP_VERSION=
      - LOG_FILE=
      - PROXIES_FILE=
      - BOT_PREFIX=
      - BOT_TOKEN=
      - CHAT_CATEGORY=
      - DEV_GUILD_ID=
      - ADDITIONAL_HIDE_ROLES=
    restart: always  # Ensures the bot restarts if it crashes
```
3. Customize the environment variables in the `docker-compose.yml` file according to your requirements. See the [Configuration](#configuration) section below for more details.

4. Run the following command to start the bot:
```bash
docker-compose up -d
```
This command will pull the latest Docker image of the ChatGPT Discord bot (if not already present) and start the bot in detached mode (`-d`). 

5. Continue the installation by following the [Running the bot](#running-the-bot) section below.

## Running the bot
1. Run the following command to start the bot:
```bash
python main.py
```
This command will start the bot in the terminal. You can now invite the bot to your server and sync the commands with the 2 following commands to ensure the bot is working properly:
```
.sync
```
and
```
.sync YOUR_GUILD_ID
```
Syncing only needs to be done when the commands are updated/added or the first time the bot is added to the server.
2. Enjoy!

## Configuration
Don't use quotes or double quotes in the values of the environment variables. All the values are required unless specified otherwise.
```yaml
#[Path]
# String, Path to the data directory (Example: /home/kway/docker/chatgpt-discord-bot)
DATA_PATH=

# [APP]
# String, URL to the bot logo (Example: https://example.com/logo.png)
APP_LOGO=

# String, Name of the bot (Example: AI Bot)
APP_NAME=

# String, URL to the bot website (Example: https://example.com)
APP_URL=

# Number, Version of the bot (Example: 1.0.0)
APP_VERSION=

# String, Path to the log file (Example: data/logs/chatgpt_bot.log)
LOG_FILE=

# !! [NOT REQUIRED] !!
# String, Path to the proxies file (Example: data/proxies/proxies.txt)
PROXIES_FILE=

# [BOT]
# String, Prefix for the bot commands (Example: .)
BOT_PREFIX=

# String, Token of the bot (Example: YOUR_BOT_TOKEN)
BOT_TOKEN=

# Integer, Category ID for the chat channels to be created (Example: YOUR_CATEGORY_ID)
CHAT_CATEGORY=

# Integer, Guild ID for the development guild (Example: YOUR_GUILD_ID)
DEV_GUILD_ID=

# List, List of roles to hide the created channels from (Example: [ROLE_ID_1, ROLE_ID_2])
ADDITIONAL_HIDE_ROLES=
```

## License
This project is licensed under the GNU License - see the [LICENSE](LICENSE) file for details.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Thanks to [xtekky](https://github.com/xtekky) for the wrapper!
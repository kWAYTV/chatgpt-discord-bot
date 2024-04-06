# AI Bot
 > ChatGPT Discord bot, easily integrate AI into your server!

## Table of contents
- [AI Bot](#ai-bot)
  - [Table of contents](#table-of-contents)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [To-Do](#to-do)
  - [License](#license)
  - [Contributing](#contributing)

## Requirements
- Discord Bot
- Python 3.8 or higher

## Installation
1. Clone the repository
2. Install the requirements with the following command:
```bash
python -m pip install -r requirements.txt
```
3. Fill the `config.yaml` file with your the needed details, see [Configuration](#configuration) for more information.
4. Run the bot with the following command:
```bash
python main.py
```
5. Invite the bot to your server & sync the commands with the 2 following commands:
```
.sync
```
and
```
.sync YOUR_GUILD_ID
```
6. Enjoy!

## Configuration
Don't use quotes or double quotes in the values of the configuration file.
```yaml
# [APP]
app_logo: # String, URL to the bot logo (Example: https://example.com/logo.png)
app_name: # String, Name of the bot (Example: AI Bot)
app_url: # String, URL to the bot website (Example: https://example.com)
app_version: # Number, Version of the bot (Example: 1.0.0)
log_file: # String, Path to the log file (Example: ai_bot.log)

# [BOT]
bot_prefix: # String, Prefix for the bot commands (Example: .)
bot_token: # String, Token of the bot (Example: YOUR_BOT_TOKEN)
chat_category: # Integer, Category ID for the chat channels to be created (Example: YOUR_CATEGORY_ID)
dev_guild_id: # Integer, Guild ID for the development guild (Example: YOUR_GUILD_ID)
additional_hide_roles: [] # List, List of roles to hide the created channels from (Example: [ROLE_ID_1, ROLE_ID_2])
```

## To-Do
- [ ] Keep conversation context between room messages
- [ ] Make the bot listen to room messages instead of pressing prompt button

## License
This project is licensed under the GNU License - see the [LICENSE](LICENSE) file for details.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
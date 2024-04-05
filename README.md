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
app_logo: # String, URL to the app logo
app_name: # String, Name of the app
app_url: # String, URL to the app
app_version: # Number, Version of the app
log_file: # String, Path to the log file (Example: ai_bot.log)

# [BOT]
bot_prefix: # String, Prefix for the bot
bot_token: # String, Token of the bot
chat_category: # Integer, Category ID for the chat channels to be created
dev_guild_id: # Integer, Guild ID for the development guild
```

## To-Do
- [ ] Keep conversation context between room messages
- [ ] Make the bot listen to room messages instead of pressing prompt button

## License
This project is licensed under the GNU License - see the [LICENSE](LICENSE) file for details.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
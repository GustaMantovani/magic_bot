# Discord MTG Bot

Welcome to the Discord MTG Bot repository! This bot provides Magic: The Gathering (MTG) card information and translations within the Discord platform.

## Features

- **Card Information**: Retrieve detailed information about MTG cards, including mana cost, type, rarity, artist, and more.
- **Card Name Translation**: Translate MTG card names from one language to another, facilitating communication among players of different linguistic backgrounds.
- **Help Command**: Accessible help command to guide users on how to interact with the bot effectively.

## Installation

To use the Discord MTG Bot, follow these steps:

1. Clone the repository to your local machine.
2. Install the required dependencies by running running the setup.sh script.
3. Set up a Discord bot application and obtain its API key.
4. Create a `.env` file and add your Discord bot API key using the format `DISCORD_API_KEY=your_api_key_here`.
5. Run the bot script using `python bot.py`.

## Usage

Once the bot is running, users can interact with it using the following commands:

- `Magic info [lang] [cardName]`: Get information about MTG cards.
- `Magic tr [original_lang] [cardName] [target_lang]`: Translate MTG card names into other languages.
- `Magic help [lang]`: Get help information.

## Acknowledgements

- Special thanks to the developers of the `discord.py` library and the MTG API for making this project possible.

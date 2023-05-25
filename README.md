# TwitchBot

TwitchBot is a Python-based chat bot for Twitch. It provides various features and commands that can be used in Twitch chat.

## Features

- **Points System**: Assigns points to users in the chat and allows them to check their points.
- **Dad Jokes**: Retrieves random dad jokes from an API and sends them to the chat.
- **Dice Roll**: Allows users to roll a dice and win or lose points based on the result.
- **Command List**: Provides a list of available commands for users to reference.
- **Runs Tracker**: Manages a list of completed runs and allows users to add or remove runs from the list.
- **Quiz**: Asks trivia questions and rewards users with points for correct answers.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/tamusandesh99/TwitchBot.git

    Install the required dependencies:

    bash

pip install -r requirements.txt

Set up the configuration file
The bot requires a configuration file named configuration.py with the following variables:
    
    TMI_TOKEN: Your Twitch chat OAuth token (can be obtained from https://twitchapps.com/tmi/)
    CLIENT_ID: Your Twitch application client ID
    BOT_NICK: The username of your bot account
    BOT_PREFIX: The prefix used for chat commands (e.g., !)
    CHANNEL: The name of the Twitch channel the bot will connect to
    MONGODB_USERNAME: Your MongoDB Atlas database username
    MONGODB_PASSWORD: Your MongoDB Atlas database password

Run the bot:

bash

    python bot.py

Usage

    Join your Twitch channel chat to start using the bot.
    Use the available commands to interact with the bot and access its features.

#Commands

    !check: Checks if the bot is connected to the chat.
    !discord: Sends a Discord server invite link.
    !dadjoke: Calls the dad joke API and sends a random dad joke to the chat.
    !points: Displays the points of the user who issued the command.
    !roll <number>: Rolls a dice with a specified number of sides and performs point calculations based on the result.
    !runs: Retrieves the list of completed runs from the database and sends it to the chat.
    !addrun <run_name>: Adds a new run name to the completed runs list in the database.
    !removerun <run_name>: Removes a run name from the completed runs list in the database.
    !commands: Displays a list of available commands.

#Main.py and BotLoop.py
To run these two files, you will need an extra monitor
      
      Edit the screen size based on your monitor and where the "You died" displays
      Run both files simultaneously  
      

Contributing

Contributions are welcome! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request.

Acknowledgments

    The Twitchio library for providing the Twitch chat integration.
    The Dad Joke API for providing the dad jokes used in the bot.

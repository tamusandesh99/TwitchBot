Twitch Bot for Elden Ring streamers

This is a Twitch bot written in Python using the twitchio library. The bot is designed to connect to a Twitch channel and perform various actions based on chat commands. It utilizes MongoDB Atlas for storing user points, completed runs, and quiz questions.


Prerequisites
Before running the bot, make sure you have the following:

    Python installed on your machine (version 3.6 or higher)
    twitchio library installed (pip install twitchio)
    pymongo library installed (pip install pymongo)
    MongoDB Atlas account and a cluster set up (for storing data)


Configuration
The bot requires a configuration file named configuration.py with the following variables:

    TMI_TOKEN: Your Twitch chat OAuth token (can be obtained from https://twitchapps.com/tmi/)
    CLIENT_ID: Your Twitch application client ID
    BOT_NICK: The username of your bot account
    BOT_PREFIX: The prefix used for chat commands (e.g., !)
    CHANNEL: The name of the Twitch channel the bot will connect to
    MONGODB_USERNAME: Your MongoDB Atlas database username
    MONGODB_PASSWORD: Your MongoDB Atlas database password

Make sure to replace the placeholder values in configuration.py with your actual credentials. For example
for CLIENT_ID: "ID"

Setup

    Clone or download the Twitch bot source code to your local machine.
    Install the required libraries mentioned in the "Prerequisites" section.
    Create the configuration.py file and set the necessary variables as described in the "Configuration" section.
    Set up a MongoDB Atlas cluster and obtain the connection URI.
    Replace the uri variable in the code with your MongoDB Atlas connection URI.
    Run the bot script using the command python bot.py.

Features
Chat Commands
The bot supports the following chat commands:

    !check: Checks if the bot is connected to the chat.
    !discord: Sends a Discord server invite link.
    !dadjoke: Calls the dad joke API and sends a random dad joke to the chat.
    !points: Displays the points of the user who issued the command.
    !roll <number>: Rolls a dice with a specified number of sides and performs point calculations based on the result.
    !add <user> <points>: Mod-only command to add points to a user in the chat.
    !runs: Retrieves the list of completed runs from the database and sends it to the chat.
    !addrun <run_name>: Adds a new run name to the completed runs list in the database.
    !removerun <run_name>: Removes a run name from the completed runs list in the database.
    !quiz: Starts a quiz by sending a random unanswered question to the chat.
    !commands: Displays a list of available commands.


Additional Features

    The bot automatically assigns points to users based on their chat activity.

How does Main.py work?
    
    Have a second monitor open, the bot takes screenshot of every frame and finds a text that equals "you died:
    If a stream fails then it adds a count to the json file
    
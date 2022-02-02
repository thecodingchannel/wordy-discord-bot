# Wordy Discord Bot
Wordy is a Wordle-like Discord bot but with a twist. It already supports 6 languages from the beginning:
English, Italian, French, German, Norwegian (Bokmål) and Austrian.
Wordy also supports colorblind mode and saves it for each user seperately.

## The Bot

Wordy uses [Disnake](https://docs.disnake.dev/en/latest/) to connect to the Discord API. Disnake was chosen to support slash commands. You must create a bot and access token within Discord before proceeding, saving it in the `.env` file.

## The Backend

The stats of the players and their games are saved in a json database file. The path to the database can be changed in the .env file's `DATABASE_PATH` variable.

Games can then be played in text-rooms and also per direct message to the bot itself.

## Setup and Requirements

This project requires you to have/install the following software before you begin:

 * Python 3.10+
 * Pipenv

To get started use this command to install a Python virtual environment with the required libraries:
```
pipenv sync --python 3.10
pipenv shell
```

Alternatively to install the dependencies in your global Python install use `pip install -U python-dotenv disnake pydantic`.

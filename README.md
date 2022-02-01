# Wordy Discord Bot
Wordy is a Wordle-like Discord bot but with a twist. It already supports 6 languages from the beginning:
English, Italian, French, German, Norwegian (Bokmål) and Austrian.

## The Bot

Wordy uses [Disnake](https://docs.disnake.dev/en/latest/) to connect to the Discord API. Disnake was chosen to support slash commands. You must create a bot and access token within Discord before proceeding, saving it in the `.env` file.

## The Backend

Wordy connects to a Notion Database to save scores. To set up your own database go to http://notion.so create an account
and workspace and an inline database. Create an integration on https://developers.notion.com/ and share the database with the integration.
The Database ID and the Notion access token should then be put into the `.env` file.

The following columns are needed:
- Title-column: User
- Number-column: DiscordID
- Text-column: LastLang
- Number-column: Win
- Number-column: Lose
- Number-column: Surrender

The bot uses the Notion database to record stats for the `/stat` command for for your entertainment.

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

Alternatively to install the dependencies in your global Python install use `pip install -U python-dotenv disnake notion-client`.

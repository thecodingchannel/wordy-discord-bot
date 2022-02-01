# Wordy Discord Bot
Wordy is a Wordle-like Discord bot but with a twist. It already supports 6 languages from the beginning:
English, Italian, French, German, Norwegian (Bokmål) and Austrian.

## The Bot

Wordy uses Disnake https://docs.disnake.dev/en/latest/ to connect to Discords API. Disnake was chosen to support Slash-Commands

## The Backend

Wordy connects to a Notion Database to save scores. To set up your own database go to http://notion.so create an account
and workspace and an inline database. Create an integration on https://developers.notion.com/ and share the database with the integration.
The Database ID will then be put into the .env file. 

The following columns are needed: 
- Title-column: User
- Number-column: DiscordID
- Text-column: LastLang
- Number-column: Win
- Number-column: Lose
- Number-column: Surrender

The bot will use the information out of that database to track the players games and performance for the /stat command. 

Games can then be played in text-rooms and also per direct message to the bot itself. 


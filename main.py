'''
This file contains the Discord interaction, implemented using the Disnake library.
'''
from typing import Callable
from dotenv import load_dotenv
load_dotenv()

import os
import traceback

import disnake
from disnake.ext import commands

from wordy_types import EndResult
from game_store import get_info_for_user, set_info_for_user, write_to_disk
from wordy_chat import begin_game, enter_guess, get_emotes_for_colorblind, render_result
from dictionary import languages, get_acceptable_words_for, get_alphabet_for, get_solution_words_for


bot = commands.Bot(command_prefix="/", description="Wordy Guessing Game", help_command=None,
    activity=disnake.Game(name='with dictionaries'))


def generate_game_commands(languages: dict):
    '''For each language we support, generate a prefix command and a slash command.'''
    for lang_code, lang in languages.items():

        def make_commands(lang_code):
            async def handle_lang_prefix(ctx: commands.Context, guess: str):
                nonlocal lang_code
                await handle_new_guess(guess, lang_code, ctx.author, ctx.reply)

            async def handle_lang_slash(inter, guess:str):
                nonlocal lang_code
                await handle_new_guess(guess, lang_code, inter.author, inter.response.send_message)

            return handle_lang_prefix, handle_lang_slash

        handle_lang_prefix, handle_lang_slash = make_commands(lang_code)
        bot.command(name=lang['command'], help=lang['help'])(handle_lang_prefix)
        bot.slash_command(name=lang['command'], description=lang['help'])(handle_lang_slash)


# Fixed prefix commands

HELP_TEXT_PRE = """**Wordy is a Wordle-like clone that supports multiple languages.**

Choose the command fitting to the language you want to use and guess a word. If Wordy returns a gray icon ⬛ the letter does not exist. If it returns a yellow icon 🟨 the letter exists but is on the wrong spot. If Wordy returns a green icon 🟩 the letter is on the correct spot.

In colorblind mode 🟦 represents the right letter on the wrong position and 🟧 the right letter on the right position.

**To enter a guess (games are started automatically):** ```
"""

HELP_TEXT_POST = """```
To give up (or to switch languages) use `/surrender`.
To toggle colorblind mode on or off use `/colorblind`.

*Wordy saves your DiscordID together with your Discord name and your game stats to provide game statistics.*
"""

@bot.command(name='surrender', help="Give up and reveal the word!")
async def surrender_prefix(ctx: commands.Context):
    await handle_surrender(ctx.author, ctx.reply)

@bot.command(name='help', help="Get your stats")
async def help_prefix(ctx: commands.Context):
    await handle_help(ctx.reply)

@bot.command(name='stats', help="Get your stats")
async def stats_prefix(ctx: commands.Context):
    await handle_stats(ctx.author, ctx.reply)

@bot.command(name='colorblind', help="Toggle colorblind mode on or off")
async def colorblind_prefix(ctx: commands.Context):
    await handle_colorblind(ctx.author, ctx.reply)

@bot.command(name='show', help="Show current board state")
async def show_prefix(ctx: commands.Context):
    await handle_show(ctx.author, ctx.reply)


# Fixed slash commands


@bot.slash_command(name='surrender', description="Give up and reveal the word!")
async def surrender_slash(inter):
    await handle_surrender(inter.user, inter.response.send_message)

@bot.slash_command(name='help', description="How to play Wordy")
async def help_slash(inter):
    await handle_help(inter.response.send_message)

@bot.slash_command(name='stats', description="Get your stats")
async def stats_slash(inter):
    await handle_stats(inter.user, inter.response.send_message)

@bot.slash_command(name='colorblind', description="Toggle colorblind mode on or off")
async def colorblind_slash(inter):
    await handle_colorblind(inter.user, inter.response.send_message)

@bot.slash_command(name='show', description="Show current board state")
async def show_slash(inter):
    await handle_show(inter.user, inter.response.send_message)


# Common functionality


async def handle_show(user: disnake.User|disnake.Member, reply: Callable):
    # Show the current board state
    player = get_info_for_user(user.id)

    if player.current_game is None:
        await reply("You haven't started a game yet!")
        return

    # Render the results
    description = "Your board:\n"
    description += "```"
    for result,word in zip(player.current_game.results, player.current_game.board_state):
        description += f"{render_result(result, player.settings.colorblind)} {word}\n"
    description += "```"

    await reply(description)


async def handle_colorblind(user: disnake.User|disnake.Member, reply: Callable):
    # Toggle colorblind state for the user
    player = get_info_for_user(user.id)
    player.username = str(user)
    player.settings.colorblind = not player.settings.colorblind
    set_info_for_user(user.id, player)
    write_to_disk()

    emote_absent, emote_present, emote_correct = get_emotes_for_colorblind(player.settings.colorblind)

    description = f"""Colorblind mode is turned {'ON' if player.settings.colorblind else 'OFF'} for you.

Your icon colors are: absent letter {emote_absent}, wrong position {emote_present}, and correct {emote_correct}."""

    await reply(description)


async def handle_help(reply: Callable):
    description = HELP_TEXT_PRE

    for lang in languages.values():
        command = f"/{lang['command']} <guess>"
        description += f"{command:<19} {lang['help']}\n"

    description += HELP_TEXT_POST

    await reply(description)


async def handle_stats(user: disnake.User|disnake.Member, reply: Callable):
    try:
        player = get_info_for_user(user.id)
        stats = player.stats
    except Exception as ex:
        print(f"Failed to fetch stats for {user}:")
        traceback.print_exc()
        await reply(f"Sorry, we're unable to fetch your stats right now 😿")
        return

    embed = disnake.Embed(title=f"{user.name}'s stats", color=0x00ff00)
    embed.set_thumbnail(url=user.avatar.url if user.avatar else None)

    embed.add_field(name="🏆 Won", value=stats.wins, inline=True)
    embed.add_field(name="☠️ Lost", value=stats.losses, inline=True)
    embed.add_field(name="🏳️ Surrendered", value=stats.surrenders, inline=False)

    embed.add_field(name='═══════════════════════', value="Games played in different languages:", inline=False)
    for lang,lang_count in player.stats.games.items():
        flag = 'gb' if lang == 'en' else lang
        embed.add_field(name=f"{lang} :flag_{flag}:", value=f"{lang_count}", inline=True)

    await reply(embed=embed)


async def handle_surrender(user: disnake.User | disnake.Member, reply: Callable):
    player = get_info_for_user(user.id)
    player.username = str(user)
    if player.current_game is None:
        await reply("You haven't started a game yet!")
        return

    player.stats.surrenders += 1
    lang_games = player.stats.games.get(player.current_game.lang, 0)
    player.stats.games[player.current_game.lang] = lang_games + 1
    answer = player.current_game.answer
    player.current_game = None
    set_info_for_user(user.id, player)

    await reply(f"You coward! 🙄\nYour word was `{answer}`!")


async def handle_new_guess(guess: str, lang: str, user: disnake.User|disnake.Member, reply: Callable):
    # Validate input
    if not guess:
        await reply(f"To play Wordy simply type `/wordy <guess>` to start or continue your own personal game.")
        return

    guess = guess.lower()
    if len(guess) != 5:
        await reply("Guess must be 5 letters long")
        return

    # Make sure the word is valid
    if guess not in get_solution_words_for(lang) and guess not in get_acceptable_words_for(lang):
        await reply("That's not a valid word!")
        return

    # Gather text to return to the user
    description = ''

    # Make sure we have a game running, starting a new one if not
    player = get_info_for_user(user.id)
    player.username = str(user)
    if not player.current_game or player.current_game.state != EndResult.PLAYING:
        description += "Starting a new game...\n"
        player.current_game = begin_game(player, lang)

    # Make sure the user isn't switching languages
    if player.current_game.lang != lang:
        await reply('You are already playing in a different language! Use `/surrender` to end it.')
        return

    # Make sure the user hasn't already guessed this word
    if guess in player.current_game.board_state:
        await reply("You've already guessed that word!")
        return

    # Make sure the guess uses only letters from the language's dictionary
    dictionary = get_alphabet_for(lang)
    if any(char not in dictionary for char in guess):
        await reply(f"You can only use the following letters: `{dictionary}`")
        return

    # Process the guess
    enter_guess(guess, player.current_game)

    # Render the results
    description += "Your results so far:\n"
    description += "```"
    for result,word in zip(player.current_game.results, player.current_game.board_state):
        description += f"{render_result(result, player.settings.colorblind)} {word}\n"
    description += "```"

    # See if the game is over
    if player.current_game.state == EndResult.WIN:
        description += f"\nCongratulations! 🎉\nCompleted in {len(player.current_game.board_state)} guesses!\n"
        player.stats.wins += 1
    elif player.current_game.state == EndResult.LOSE:
        description += f"\nNo more guesses! 😭\nYour word was `{player.current_game.answer}`!\n"
        player.stats.losses += 1

    # Send the response
    embed = disnake.Embed(title="Wordy", description=description.strip('\n'))
    await reply(embed=embed)

    # If the game is done, record stats and remove game data
    if player.current_game.state != EndResult.PLAYING:
        lang_games = player.stats.games.get(player.current_game.lang, 0)
        player.stats.games[player.current_game.lang] = lang_games + 1
        player.current_game = None

    # Store the updated player info
    set_info_for_user(user.id, player)
    write_to_disk()



if __name__ == "__main__":
    generate_game_commands(languages)
    bot.run(os.getenv("DISCORD_TOKEN"))

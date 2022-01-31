import os
import disnake

from notion_client import AsyncClient

from wordy_types import EndResult


if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()


notion = AsyncClient(auth=os.getenv('NOTION_SECRET'))
db_id = os.getenv('DB_ID')


def get_number(property):
    assert property['type'] == 'number'
    return property['number']


async def report_game_stats(user: disnake.User|disnake.Member, result: EndResult, lang: str):
    # Find the user's existing entry in the database
    results = await notion.databases.query(db_id, filter={'property': 'DiscordID', 'number': {'equals': user.id}})

    if len(results['results']):
        # Update existing entry
        page = results['results'][0]

        # Always set the last known username and selected language
        updates = {
            'User': { 'title': [{'text': {'content': str(user)}}] },
            'LastLang': { 'rich_text': [{'text': {'content': lang}}] },
        }

        # Update the result stats
        if result == EndResult.WIN:
            updates['Win'] = { 'number': get_number(page['properties']['Win']) + 1 }
        elif result == EndResult.LOSE:
            updates['Lose'] = { 'number': get_number(page['properties']['Lose']) + 1 }
        elif result == EndResult.SURRENDER:
            updates['Surrender'] = { 'number': get_number(page['properties']['Surrender']) + 1 }

        # Send the update
        await notion.pages.update(page['id'], properties=updates)
    else:
        # Create new entry for the user
        page = {
            'User': { 'title': [{'text': {'content': str(user)}}] },
            'LastLang': { 'rich_text': [{'text': {'content': lang}}] },
            'DiscordID': { 'number': user.id },
            'Win': { 'number': 0 },
            'Lose': { 'number': 0 },
            'Surrender': { 'number': 0 },
        }

        if result == EndResult.WIN:
            page['Win']['number'] = 1
        elif result == EndResult.LOSE:
            page['Lose']['number'] = 1
        elif result == EndResult.SURRENDER:
            page['Surrender']['number'] = 1

        # Store it in the database
        await notion.pages.create(parent={'database_id':db_id}, properties=page)


async def fetch_game_stats(user: disnake.User|disnake.Member):
    # Find the user's existing entry in the database
    results = await notion.databases.query(db_id, filter={'property': 'DiscordID', 'number': {'equals': user.id}})

    if len(results['results']):
        # Update existing entry
        page = results['results'][0]

        # Return the stats
        return {
            'win': get_number(page['properties']['Win']),
            'lose': get_number(page['properties']['Lose']),
            'surrender': get_number(page['properties']['Surrender']),
        }

    # Return zero for all
    return {
        'win': 0,
        'lose': 0,
        'surrender': 0,
    }



# def set_title(property, text):
#     assert property['type'] == 'title'
#     property['title'] = [
#         {
#             'type': 'text',
#             'text': { 'content': text, 'link': None },
#             'annotations': {
#                 'bold': False,
#                 'italic': False,
#                 'strikethrough': False,
#                 'underline': False,
#                 'code': False,
#                 'color': 'default'
#             },
#             'plain_text': text,
#             'href': None
#         }
#     ]

# def set_text(property, text):
#     assert property['type'] == 'rich_text'
#     property['rich_text'] = [
#         {
#             'type': 'text',
#             'text': { 'content': text, 'link': None },
#             'annotations': {
#                 'bold': False,
#                 'italic': False,
#                 'strikethrough': False,
#                 'underline': False,
#                 'code': False,
#                 'color': 'default'
#             },
#             'plain_text': text,
#             'href': None
#         }
#     ]

# def set_number(property, number):
#     assert property['type'] == 'number'
#     property['number'] = number

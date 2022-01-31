'''
This file gives fully cached access to the dictionary words.

Note that dictionaries that change on disk will be reloaded automatically.
'''

from file_reader import fetch_cached_file


languages = {
    'en': {
        'site': 'https://www.powerlanguage.co.uk/wordle/',
        'alphabet': 'qwertyuiopasdfghjklzxcvbnm',
        'command': "wordy",
        'help': "Guess a word in your own personal Wordy game! [English]",
    },
    'it': {
        'site': 'https://pietroppeter.github.io/wordle-it/',
        'alphabet': 'qwertyuiopasdfghjklzxcvbnm',
        'command': "wordy_it",
        'help': "Indovina una parola nel tuo gioco personale di Wordy! [Italiano]",
    },
    'fr': {
        'site': 'https://wordle.louan.me/',
        'alphabet': 'azertyuiopqsdfghjklmwxcvbn',
        'command': "moty",
        'help': "Devinez un mot dans votre propre jeu Moty personnel! [Français]",
    },
    'de': {
        'site': 'https://wordle.uber.space/',
        'alphabet': 'qwertzuiopasdfghjklyxcvbnm',
        'command': "wörti",
        'help': "Errate ein Wort in deinem persönlichen Wörti-Spiel! [Deutsch]",
    },
    'no': {
        'site': 'https://evancharlton.github.io/ordle/#/nb-no',
        'alphabet': 'qwertyuiopåasdfghjkløæzxcvbnm',
        'command': "wørdy",
        'help': "Gjett et ord i ditt personlige Wørdy spill!! [Norwegian Bokmål]",
    },
    'at': {
        'site': 'https://wordle.at/',
        'alphabet': 'qwertzuiopasdfghjklyxcvbnm',
        'command': "wörti_at",
        'help': "Errate ein Wort in deinem persönlichen Wörti-Spiel! [Österreichisch]",
    },
}


def get_alphabet_for(lang: str) -> str:
    return languages[lang]['alphabet']


def get_solution_words_for(lang: str) -> list[str]:
    '''
    Get the solution words for a language.
    '''
    if lang not in languages:
        raise ValueError(f'Language {lang} is not supported')

    return fetch_cached_file(f'data/{lang}/solution_words.txt', _parse_lines)


def get_acceptable_words_for(lang: str) -> list[str]:
    '''
    Get the acceptable guess words for a language.
    '''
    if lang not in languages:
        raise ValueError(f'Language {lang} is not supported')

    return fetch_cached_file(f'data/{lang}/accepted_words.txt', _parse_lines)


def _parse_lines(data: bytes) -> list[str]:
    lines = data.decode('utf-8').splitlines()
    return [word for word in lines if word]


if __name__ == '__main__':
    print(len(get_solution_words_for('en')))
    print(len(get_solution_words_for('en')))
    print(len(get_solution_words_for('fr')))


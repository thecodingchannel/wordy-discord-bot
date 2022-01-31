'''
This file contains the logic for playing a game of Wordle.
'''

import random
from typing import Iterator

from dictionary import get_solution_words_for
from wordy_types import LetterState


def evaluate_guess(guess: str, answer: str) -> Iterator[LetterState]:
    '''
    Evaluate a guess against an answer.

    >>> list(evaluate_guess("a", "a")) == [LetterState.CORRECT]
    True
    >>> list(evaluate_guess("b", "a")) == [LetterState.ABSENT]
    True
    >>> list(evaluate_guess("aa", "ab")) == [LetterState.CORRECT, LetterState.ABSENT]
    True
    >>> list(evaluate_guess("aa", "ba")) == [LetterState.ABSENT, LetterState.CORRECT]
    True
    >>> list(evaluate_guess("ac", "ba")) == [LetterState.PRESENT, LetterState.ABSENT]
    True
    >>> list(evaluate_guess("wordle", "wordle")) == [LetterState.CORRECT]*6
    True
    '''
    if len(guess) != len(answer):
        raise ValueError("Guess and answer must be of same length")

    # Count letters in the guess which aren't exactly correct
    answer_counts = {}
    for guess_letter, answer_letter in zip(guess, answer):
        if guess_letter != answer_letter:
            answer_counts[answer_letter] = answer_counts.get(answer_letter, 0) + 1

    for guess_letter, answer_letter in zip(guess, answer):
        # Letter matches
        if guess_letter == answer_letter:
            yield LetterState.CORRECT
            continue

        # Letter isn't used at all
        if answer_counts.get(guess_letter, 0) <= 0:
            yield LetterState.ABSENT
            continue

        # So the letter is used, but in the wrong place
        # Reduce the count of the letter so we don't
        # report it too many times
        answer_counts[guess_letter] -= 1
        yield LetterState.PRESENT


def generate_new_word(lang: str):
    '''
    Pick a random word as a new game solution.
    '''
    words = get_solution_words_for(lang)
    word = random.choice(words)
    return word

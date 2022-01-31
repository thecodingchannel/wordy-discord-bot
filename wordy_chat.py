'''
This part handles the game state management, with each user having their own active game.
'''

from typing import Optional

from game_store import clear_game, fetch_stored_game, store_game
from wordle_logic import evaluate_guess, generate_new_word
from wordy_types import ActiveGame, EndResult, LetterState


def begin_game(user_id: int, lang: str) -> ActiveGame:
    """
    Begin a game for a user.
    """

    # Select a word
    answer = generate_new_word(lang)

    # Create and store new game state
    new_game = ActiveGame(answer=answer, lang=lang)
    store_game(user_id, new_game)

    return new_game


def end_game(user_id: int) -> None:
    """
    End a game for a user.
    """
    clear_game(user_id)


def get_game_for_user(user_id: int) -> Optional[ActiveGame]:
    """
    Fetch the game state for a user.
    """
    return fetch_stored_game(user_id)


def enter_guess(guess: str, game: ActiveGame) -> EndResult:
    """
    Enter a guess for a user's game and reports back if the game ends.

    >>> game=ActiveGame("en", "abcd")
    >>> enter_guess("aaaa", game) == EndResult.PLAYING
    True
    >>> render_result(game.results[-1])
    '🟩⬛⬛⬛'
    >>> game=ActiveGame("en", "abca")
    >>> enter_guess("aaaz", game) == EndResult.PLAYING
    True
    >>> render_result(game.results[-1])
    '🟩🟨⬛⬛'
    >>> game=ActiveGame("en", "abca")
    >>> enter_guess("aaab", game) == EndResult.PLAYING
    True
    >>> render_result(game.results[-1])
    '🟩🟨⬛🟨'
    """
    if game.state != EndResult.PLAYING:
        return game.state

    # Evaluate guess
    result = tuple(evaluate_guess(guess, game.answer))

    # Update game state
    game.board_state.append(guess)
    game.results.append(result)

    # Check if game is over
    if result == (LetterState.CORRECT,)*len(game.answer):
        game.state = EndResult.WIN
    elif len(game.board_state) > len(game.answer):
        game.state = EndResult.LOSE

    return game.state


def render_result(result: tuple[LetterState]) -> str:
    """
    Render a result to a string.

    >>> render_result((LetterState.ABSENT, LetterState.PRESENT, LetterState.CORRECT))
    '⬛🟨🟩'
    >>> render_result((LetterState.ABSENT,)*4)
    '⬛⬛⬛⬛'
    """
    return "".join(
        "⬛" if state == LetterState.ABSENT else
        "🟨" if state == LetterState.PRESENT else "🟩"
        for state in result
    )


if __name__ == "__main__":
    # Quick chat emulator to test the game logic
    def handle_input(guess: str, user_id: int):
        game = get_game_for_user(user_id)
        if not game or game.state != EndResult.PLAYING:
            print("Starting new game!")
            game = begin_game(user_id, 'en')

        enter_guess(guess, game)

        for result,word in zip(game.results, game.board_state):
            print(f"{render_result(result)} {word}")

        if game.state == EndResult.WIN:
            print(f"Congratulations! Completed in {len(game.board_state)} guesses!")
        elif game.state == EndResult.LOSE:
            print(f"Sorry, you lost. The answer was {game.answer}")

        if game.state != EndResult.PLAYING:
            end_game(user_id)


    while True:
        guess = input("Guess: ")
        handle_input(guess, 0xdeadbeef)

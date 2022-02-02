'''
This part handles the game state management, with each user having their own active game.
'''

from game_store import get_info_for_user, set_info_for_user
from wordle_logic import evaluate_guess, generate_new_word
from wordy_types import ActiveGame, EndResult, LetterState, UserInfo


def begin_game(player: UserInfo, lang: str) -> ActiveGame:
    """
    Begin a game for a user.
    """
    if player.current_game:
        raise ValueError("User already has an active game")

    # Select a word
    answer = generate_new_word(lang)

    # Create and store new game state
    new_game = ActiveGame(answer=answer, lang=lang)

    return new_game


def enter_guess(guess: str, game: ActiveGame) -> EndResult:
    """
    Enter a guess for a user's game and reports back if the game ends.

    >>> game=ActiveGame(lang="en", answer="abcd")
    >>> enter_guess("aaaa", game) == EndResult.PLAYING
    True
    >>> render_result(game.results[-1])
    '🟩⬛⬛⬛'
    >>> game=ActiveGame(lang="en", answer="abca")
    >>> enter_guess("aaaz", game) == EndResult.PLAYING
    True
    >>> render_result(game.results[-1])
    '🟩🟨⬛⬛'
    >>> game=ActiveGame(lang="en", answer="abca")
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


def get_emotes_for_colorblind(colorblind: bool) -> tuple[str, str, str]:
    '''
    Get the emotes for to use, based on whether colorblind mode is on or off.

    Returns a tuple of the emotes for absent, present, and correct.
    '''
    if colorblind:
        return '⬛', '🟦', '🟧'
    else:
        return '⬛', '🟨', '🟩'


def render_result(result: tuple[LetterState], colorblind: bool = False) -> str:
    """
    Render a result to a string.

    >>> render_result((LetterState.ABSENT, LetterState.PRESENT, LetterState.CORRECT))
    '⬛🟨🟩'
    >>> render_result((LetterState.ABSENT, LetterState.PRESENT, LetterState.CORRECT), True)
    '⬛🟦🟧'
    >>> render_result((LetterState.ABSENT,)*4)
    '⬛⬛⬛⬛'
    """

    absent, present, correct =  get_emotes_for_colorblind(colorblind)

    return "".join(
        absent if state == LetterState.ABSENT else
        present if state == LetterState.PRESENT else correct
        for state in result
    )


if __name__ == "__main__":
    from game_store import write_to_disk

    # Quick chat emulator to test the game logic
    def handle_input(guess: str, user_id: int):
        player = get_info_for_user(user_id)

        if not player.current_game or player.current_game.state != EndResult.PLAYING:
            print("Starting new game!")
            player.current_game = begin_game(player, 'en')

        enter_guess(guess, player.current_game)

        for result,word in zip(player.current_game.results, player.current_game.board_state):
            print(f"{render_result(result)} {word}")

        if player.current_game.state == EndResult.WIN:
            print(f"Congratulations! Completed in {len(player.current_game.board_state)} guesses!")
        elif player.current_game.state == EndResult.LOSE:
            print(f"Sorry, you lost. The answer was {player.current_game.answer}")

        if player.current_game.state != EndResult.PLAYING:
            player.current_game = None

        set_info_for_user(user_id, player)

        write_to_disk()

    while True:
        guess = input("Guess: ")
        handle_input(guess, 0xdeadbeef)

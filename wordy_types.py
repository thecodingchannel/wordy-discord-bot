from enum import Enum
from dataclasses import dataclass, field


class LetterState(Enum):
    ABSENT = "absent"
    PRESENT = "present"
    CORRECT = "correct"


class EndResult(Enum):
    PLAYING = 0
    WIN = 1
    LOSE = 2
    SURRENDER = 3


@dataclass
class ActiveGame:
    lang: str
    answer: str
    board_state: list[str] = field(default_factory=list)
    results: list[tuple[LetterState, ...]] = field(default_factory=list)
    state: EndResult = field(default=EndResult.PLAYING)

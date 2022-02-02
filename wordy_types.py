from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class LetterState(str, Enum):
    ABSENT = "absent"
    PRESENT = "present"
    CORRECT = "correct"


class EndResult(int, Enum):
    PLAYING = 0
    WIN = 1
    LOSE = 2
    SURRENDER = 3


class ActiveGame(BaseModel):
    lang: str
    answer: str
    board_state: list[str] = Field(default_factory=list)
    results: list[tuple[LetterState, ...]] = Field(default_factory=list)
    state: EndResult = Field(default=EndResult.PLAYING)


class Stats(BaseModel):
    wins: int = 0
    losses: int = 0
    surrenders: int = 0
    games: dict[str, int] = Field(default_factory=dict)


class Settings(BaseModel):
    colorblind: bool = False


class UserInfo(BaseModel):
    current_game: Optional[ActiveGame] = None
    settings: Settings = Field(default_factory=Settings)
    stats: Stats = Field(default_factory=Stats)
    username: Optional[str] = None

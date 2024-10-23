from typing import List, NamedTuple, Tuple

class Gamble(NamedTuple):
    amount_bet: float
    win_percentage: float

class GambleOutcome(NamedTuple):
    amount_bet: float
    win_percentage: float
    won: bool
    amount_won: float

MutableHistory = List[bool]
History = Tuple[bool, ...]

Outcome = Tuple[float, History]

class Strategy:
    def __init__(self):
        self.name: str = ''
        self.author: str = ''
    
    def play(self, balance: float, rounds_left: int, history: History) -> Gamble:
        return

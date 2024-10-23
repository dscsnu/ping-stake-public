import math
import random

from utils.types import Gamble, History

class Strategy:
    def __init__(self):
        self.name: str = 'your_strategy_name'
        self.author: str = 'your_netid'
        
    def play(self, balance: float, rounds_left: int, history: History) -> Gamble:
        pass
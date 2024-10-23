

# @ping-stake

A compete-with-code style tournament where each player can submit their strategy to come out on top and win prizes.

## QuickStart

Please read the whole documentation before using this 😛

1. Clone this repository
2. Install requirements
3. Create a Python file under the `strategies` folder
4. Use the following skeleton and populate the functions with your logic

```python
from utils.types import Strategy, Gamble, History

class Strategy():
    def __init__(self):
        self.name = "Example Strategy"
        self.author = "author1pustakpathaka"

    def play(self, balance: float, rounds_left: int, history: History) -> Gamble:
        # always bet 1% of balance with a 60% win chance
        bet_amount = balance * 0.01
        return Gamble(bet_amount, 60)
```

5. Run the main file and ensure no errors occur.

## The Game

You have been invited to compete against other people for virtual money. Your goal is to come out with the largest sum of money at the end of all 100 rounds.

### Initial Setup:

Each player starts with a fixed amount of money (e.g., $1,000).
The game lasts for 100 rounds.

### Betting:

In each round, players decide how much money to bet from their current balance.
Players also choose a **win percentage** for each bet:
- Higher win percentages give a higher chance of winning but smaller rewards.
- Lower win percentages offer lower chances of winning but larger rewards.

### Winning Condition:

The player with the highest final balance after 100 rounds wins.  
Each strategy competes by playing all 100 rounds with the same starting conditions, and the final balances are compared.

## Tutorial

Here’s a basic example of how a strategy could be written:

```python
from utils.types import Strategy, Gamble, History

class Strategy():
    def __init__(self):
        self.name = "YOLO Strategy"
        self.author = "mueheheh"

    def play(self, balance: float, rounds_left: int, history: History) -> Gamble:
        # yolo: all-in with max risk (1% win chance)
        return Gamble(balance, 1)  # bet all, 1% win chance (max risk)
```

The `YoloStrategy` class defines an extreme, high-risk betting strategy for the game where the player bets all of their balance in each round with the maximum allowed **win chance** of 1%. Here’s a breakdown of how this strategy works:

### Key Components:
- **Strategy**: This is the parent class, likely part of the game's framework. `YoloStrategy` inherits from it.
- **Gamble**: This is likely a class that represents a bet, including how much money is wagered and the win percentage associated with it.
- **History**: This class holds the history of past bets and outcomes. However, it is not used in this strategy, meaning the strategy doesn't consider previous wins or losses.
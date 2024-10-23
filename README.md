

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

class ExampleStrategy(Strategy):
    def __init__(self):
        super().__init__()
        self.name = "Example Strategy"
        self.author = "author1pustakpathaka"

    def play(self, balance: float, rounds_left: int, history: History) -> Gamble:
        # always bet 1% of balance with a 60% win chance
        bet_amount = balance * 0.01
        return Gamble(bet_amount, 60)
```

5. Run the main file and ensure no errors occur.

## The Game

You have been invited to compete against other people for virtual money. Your goal is to come out with the largest sum of money at the end of all 1000 rounds.

### Initial Setup:

Each player starts with a fixed amount of money (e.g., $10,000).
The game lasts for 1000 rounds.

### Betting:

In each round, players decide how much money to bet from their current balance.
Players also choose a **win percentage** for each bet:
- Higher win percentages give a higher chance of winning but smaller rewards.
- Lower win percentages offer lower chances of winning but larger rewards.

### Win Percentage and Reward:

Players can choose from various win percentages with corresponding reward multipliers:
- 50% win chance: 50% chance to double the bet. If you win, you earn 2x your bet. If you lose, you lose the entire bet.
- 10% win chance: 10% chance to win 10x your bet.
- 1% win chance: 1% chance to win 100x your bet.

### Winning Condition:

The player with the highest final balance after 1000 rounds wins.  
Each strategy competes by playing all 1000 rounds with the same starting conditions, and the final balances are compared.

## Tutorial

Here’s a basic example of how a strategy could be written:

```python
from utils.types import Strategy, Gamble, History

class YoloStrategy(Strategy):
    def __init__(self):
        super().__init__()
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

## Another Strategy

Let's take a look at another strategy:

```python
from utils.types import Strategy, Gamble, History

class AdaptiveStrategy(Strategy):
    def __init__(self):
        super().__init__()
        self.name = "Adaptive Strategy"
        self.author = "careful_player"
    
    def play(self, balance: float, rounds_left: int, history: History) -> Gamble:
        # Check if there is any previous history
        if len(history) == 0:
            # First round, bet conservatively
            return Gamble(balance * 0.05, 90)  # Bet 5% of balance, 90% win chance

        # Get outcome of the last round
        last_round = history[-1]
        last_outcome = last_round['outcome']  # Assuming 'outcome' is either 'win' or 'loss'

        if last_outcome == 'win':
            # If the last round was a win, bet more aggressively
            bet_amount = balance * 0.20  # Bet 20% of the balance
            win_percentage = 50  # 50% win chance, higher reward
        else:
            # If the last round was a loss, bet conservatively
            bet_amount = balance * 0.05  # Bet 5% of the balance
            win_percentage = 90  # 90% win chance, lower risk

        return Gamble(bet_amount, win_percentage)
```

### Explanation:

- **Initialization**:
    - `name = "Adaptive Strategy"`: This strategy adjusts based on recent outcomes.
    - `author = "careful_player"`: This strategy is meant to be cautious, betting larger after wins and reducing bets after losses.

- **The play Method**:
    - `history` is checked: If there is no history (i.e., this is the first round), the strategy bets conservatively, using 5% of the balance with a 90% win chance.
    
- **After a win**:
    - If the player won the last round, the strategy bets more aggressively, risking 20% of the balance with a 50% win chance, which offers a larger potential reward.
    
- **After a loss**:
    - If the player lost the last round, the strategy becomes more cautious, betting only 5% of the balance with a 90% win chance, minimizing the chance of losing even more.
    
- **Dynamic Betting**:
    - The strategy uses the player's recent history to adjust its betting style. A win increases the risk for potential high gains, while a loss reduces the risk to preserve capital.
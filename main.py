import os
import ast
import time
import requests
import importlib.util
from pathlib import Path
from typing import Any
from tqdm import tqdm

from utils.types import Gamble, Strategy, MutableHistory, Outcome

def load_strategy(filename: str) -> Any:
    STRATEGIES_PATH = Path("./strategies")
    file_path = STRATEGIES_PATH / filename

    ALLOWED_IMPORTS = {
        'math', 'random'
    }

    ALLOWED_IMPORTS_FROM = {
        ('utils.types', 'Gamble'),
        ('utils.types', 'History'),
    }

    with open(file_path, 'r') as file:
        tree = ast.parse(file.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'print':
                raise ValueError(f"Print statement found in {filename}. Print statements are not allowed in strategy files.")

            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name not in ALLOWED_IMPORTS:
                        raise ValueError(f"Unauthorized import '{alias.name}' found in {filename}. Only 'math' and 'random' are allowed")

            if isinstance(node, ast.ImportFrom):
                module_name = node.module
                for alias in node.names:
                    if (module_name, alias.name) not in ALLOWED_IMPORTS_FROM:
                        raise ValueError(f"Unauthorized import from '{module_name}' found in {filename}. Only 'from utils.types import Gamble, History' is allowed.")

    spec = importlib.util.spec_from_file_location(filename[:-3], file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if hasattr(module, "Strategy"):
        return getattr(module, "Strategy")
    raise AttributeError("Strategy class not found in the module")

def run_trajectory(strategy: Strategy, balance: float, num_rounds: int) -> Outcome:
    history: MutableHistory = []

    start_time = time.time()

    with tqdm(total=num_rounds, desc="Running trajectory", unit="round", bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{rate_fmt}{postfix}]') as pbar:
        for round in range(1, num_rounds + 1):

            if (balance <= 0):
                break

            gamble = strategy.play(balance, num_rounds - round, history=tuple(history))

            if not isinstance(gamble, Gamble):
                raise TypeError(f"Invalid move type. Expected Gamble, got {type(gamble)}")

            # cannot bet more than balance
            # cannot bet with zero win percentage
            # cannot bet with win percentage greater than 100
            if (gamble.amount_bet > balance or gamble.win_percentage <= 0 or gamble.win_percentage > 100):
                continue

            # run gamble
            balance -= gamble.amount_bet

            try:
                response = requests.get(
                    'https://stake-api-b79578c75931.herokuapp.com/gamble',
                    params = {
                        'amount_bet': gamble.amount_bet,
                        'win_percentage': gamble.win_percentage,
                    }
                )
                response_data: dict = response.json()

                balance += response_data.get('amount_won', 0)
                history.append(response_data.get('won', False))
            except requests.RequestException as e:
                print(f'Request Error: {e}')

            pbar.update(1)
            elapsed_time = time.time() - start_time
            pbar.set_postfix({'Time': f'{elapsed_time:.2f}s'})

        return ( balance, history )

def main() -> None:
    INTIAL_BALANCE: float = 1_000.0
    NUM_ROUDS: int = 100
    TIMEOUT_SECONDS: int = 5 * 60

    try:
        # Find the strategy file in the strategies folder
        strategy_file = next(file for file in os.listdir("./strategies") if file.endswith(".py") and file != "__init__.py")

        try:
            StrategyClass = load_strategy(strategy_file)
        except ValueError as e:
            print(f"Error in strategy file: {str(e)}")
            return

        test_strategy = StrategyClass()
        start_time = time.time()

        outcome: Outcome = run_trajectory(test_strategy, INTIAL_BALANCE, NUM_ROUDS)
        print(outcome)
    
        end_time = time.time()
        total_time = end_time - start_time

        if total_time > TIMEOUT_SECONDS:
            print(f"\nTest failed: Execution time ({total_time:.2f} seconds) exceeded the {TIMEOUT_SECONDS / 60}-minute limit.")
        else:
            print(f"\nTest passed: Execution completed in {total_time:.2f} seconds.")

    except Exception as e:
        print(f"\nError occurred during test execution: {str(e)}")

if __name__ == "__main__":
    main()

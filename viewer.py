import os
import json
import glob

# Setup variables
ENTERANCE_COST = 3

DOUBLE_REWARD_REVEAL = 5
TRIPLE_REWARD_REVEAL = 10
QUAD_REWARD_REVEAL = 20
FIVE_REWARD_REVEAL = 43

DOUBLE_REWARD_STACK = 5
TRIPLE_REWARD_STACK = 10
QUAD_REWARD_STACK = 20
FIVE_REWARD_STACK = 43

# List of prizes
REWARDS_STACK = [0, 0, DOUBLE_REWARD_STACK,
                 TRIPLE_REWARD_STACK, QUAD_REWARD_STACK, FIVE_REWARD_STACK]

REWARDS_REVEAL = [0, 0, DOUBLE_REWARD_REVEAL,
                  TRIPLE_REWARD_REVEAL, QUAD_REWARD_REVEAL, FIVE_REWARD_REVEAL]

# List of winner couter
WINNERS_STACK = [0, 0, 0, 0, 0, 0]
WINNERS_REVEAL = [0, 0, 0, 0, 0, 0]

# Get list of game files
file_names = glob.glob("data/results-*.json")


# Nice formatter to be used when printing
class Formatter():
    total = 0

    def set_total(total):
        Formatter.total = total

    def number(val):
        return "{:,}".format(val)

    def percent(val, padding=True):
        space = " " if padding and val / Formatter.total < 1 else ""
        return f"{space}{100 * val / Formatter.total:.3f}%"

    def summed_percent(val, padding=True):
        return f"{100 * sum(val) / Formatter.total:.3f}%"


for bank_account in glob.glob("data/bank-*.json"):
    os.remove(bank_account)

i = 0
# Setup a "bank"
bank = 0
bank_history = [bank]
for file_name in file_names:
    with open(file_name) as games:
        results = json.load(games)

        # Loop through every game
        for result in results:
            i += 1
            if i % 100000 == 0:
                bank_history.append(bank)
                if i % 10000000 == 0:
                    with open(f'data/bank-{i//1000000}.json', 'w') as bank_results:
                        json.dump(bank_history, bank_results)
                    bank_history = []

            # Pay money to start the game
            bank -= ENTERANCE_COST

            # Get the number of cards revealed and the largest stack
            revealed_count = len(result) - result.count(0)
            largest_stack = max(result)

            # If over 5 in a stack, add to winners list (and extend if needed)
            if largest_stack > 5:
                while len(WINNERS_STACK) <= largest_stack:
                    WINNERS_STACK.append(0)
                WINNERS_STACK[largest_stack] += 1
                continue

            # Check which reward is largest
            # Add 1 to winner counts
            # Add reward to bank
            if REWARDS_REVEAL[revealed_count] >= REWARDS_STACK[largest_stack]:
                WINNERS_REVEAL[revealed_count] += 1
                bank += REWARDS_REVEAL[revealed_count]
            else:
                WINNERS_STACK[largest_stack] += 1
                bank += REWARDS_STACK[largest_stack]

            # Print bank account each iteration
            print(f"${Formatter.number(bank)}")


# Grab total number of games played
games_played = sum(WINNERS_STACK) + sum(WINNERS_REVEAL)

Formatter.set_total(games_played)

# Set losers to anything with no pay off (0 or 1)
LOSERS = [WINNERS_REVEAL[0] + WINNERS_STACK[0],
          WINNERS_REVEAL[1] + WINNERS_STACK[1]]

# Fix winner reveal and stack lits
WINNERS_REVEAL = WINNERS_REVEAL[2:]
WINNERS_STACK = WINNERS_STACK[2:]

# Pretty print everything
print()

# Print all totals
print(f"Completed Number of Games: {Formatter.number(games_played)}")
print(f"Final Bank Value: ${Formatter.number(bank)}")
print(f"Average Winning of ${bank/games_played:.8f}")

print()

# Print stats about losers, reveal winners, and stack winners
print(f"Losers ({Formatter.summed_percent(LOSERS)}):")
for i, loser in enumerate(LOSERS):
    print(f"\t{i}:\t{Formatter.percent(loser)}")

print(f"Reveal Winners ({Formatter.summed_percent(WINNERS_REVEAL)}):")
for i, winner in enumerate(WINNERS_REVEAL):
    print(f"\t{i+2}:\t{Formatter.percent(winner)}")

print(f"Stack Winners ({Formatter.summed_percent(WINNERS_STACK)}):")
for i, winner in enumerate(WINNERS_STACK):
    print(f"\t{i+2}:\t{Formatter.percent(winner)}")

data = {
    "LOSERS": LOSERS,
    "WINNERS_REVEAL": WINNERS_REVEAL,
    "WINNERS_STACK": WINNERS_STACK
}

with open('data/placements.json', 'w') as results:
    json.dump(data, results)

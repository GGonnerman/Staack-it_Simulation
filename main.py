from random import shuffle, choice
from json import dump
import time
import math
import glob
import os

# Editable variables

NUMBER_OF_CARDS = 5
NUMBER_OF_GAMES = 1000000000
FILE_PARTS = 1000

# When to break into multiple files
file_cuts = math.floor(NUMBER_OF_GAMES / FILE_PARTS)

# Wild cards, can be placed anywhere
WILD_CARDS = {12, 13}
GOOD_CARDS = set()
# Good cards, a list of all cards on the pile
for i in range(NUMBER_OF_CARDS):
    GOOD_CARDS.add(i)
# All cards that could be played
ALL_CARDS = {*GOOD_CARDS, *WILD_CARDS}


def play_game():

    # Create and shuffle a deck
    deck = [0, 0, 0, 0,      # Ace
            1, 1, 1, 1,      # 2
            2, 2, 2, 2,      # 3
            3, 3, 3, 3,      # 4
            4, 4, 4, 4,      # 5
            5, 5, 5, 5,      # 6
            6, 6, 6, 6,      # 7
            7, 7, 7, 7,      # 8
            8, 8, 8, 8,      # 9
            9, 9, 9, 9,      # 10
            10, 10, 10, 10,  # Jack
            11, 11, 11, 11,  # Queen
            12, 12, 12, 12,  # King
            13, 13]          # Joker
    shuffle(deck)

    # Generate a pile of cards
    pile = [0, 0, 0, 0, 0]

    # Create an empty hand
    hand = None

    # Flip over the revealed card
    revealed_card = deck.pop()

    # If revealed card is playable grab that
    # Otherwise pick top card from deck
    if revealed_card in ALL_CARDS:
        hand = revealed_card
    else:
        hand = deck.pop()

    # While the card is still playable
    while hand in ALL_CARDS:
        # Index of hand
        chosen_index = hand
        
        if hand in WILD_CARDS:
            # Check number of not flipped and largest stack
            turned = len(pile) - pile.count(0)
            highest = max(pile)
            # If everything is turned over, don't try to turn more over
            if turned == len(pile):
                turned = -1
            # Continue on the best trend
            # flip if more flipped, stack if more stacked
            if turned > highest:
                chosen_index = pile.index(0)
            elif turned < highest:
                chosen_index = pile.index(highest)
            else:
                # Chosen randomly between the two if tied
                chosen_index = choice([pile.index(0), pile.index(highest)])
        # Add one to number on stack
        pile[chosen_index] += 1
        # Grab card from deck
        hand = deck.pop()
    return pile


# Start timer
begin = time.time()

# Make sure data folder exists
if not os.path.exists('data'):
    os.mkdir('data')

# Remove old game files
for file_name in glob.glob("data/results-*.json"):
    os.remove(file_name)

games = []
# Run games x times and store results
for i in range(1, NUMBER_OF_GAMES + 1):
    games.append(play_game())
    # If at a cut point, write data and reset game list
    if i % file_cuts == 0:
        print(f'Writing data/results-{i}.json...')
        with open(f'data/results-{i}.json', 'w') as speed_games:
            dump(games, speed_games)
        games = []

# Print final execution time
end = time.time()
print(f"Execution Time in Seconds: {end - begin}")

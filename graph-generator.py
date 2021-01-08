import matplotlib.pyplot as plt
from numpy import arange
import glob
import json

# Grab data from bank file
bank_file_names = glob.glob('data/bank-*.json')
bank_files = []
for file_name in bank_file_names:
    file_id = file_name.split('-')[1].split('.')[0]
    bank_files.append(int(file_id))

bank_history = []
for num in sorted(bank_files):
    with open(f'data/bank-{num}.json') as bank_file:
        bank_history += json.load(bank_file)

# Number of points to have on x-axis
count = 10

# Generate x axis labels
x_labels = [i for i in range(0, len(bank_history), len(bank_history) // count)]

# Scale x-axis to millions
x_labels = [x // 10 for x in x_labels]
# Scale y-axis to thousands
bank_history = [b / 1000 for b in bank_history]

# Plot it
plt.plot(bank_history)
# Add correctly placed tick marks
plt.xticks(arange(0, len(bank_history), step=len(bank_history) // count),
           x_labels)
# Add Labels
plt.title("Bank Net Worth Over Time")
plt.ylabel("Money (thousands)")
plt.xlabel("Number of iterations (millions)")

# Show the plot
plt.show()

with open('data/placements.json') as placement_data:
    placements = json.load(placement_data)
    placements["WINNERS_STACK"] = placements["WINNERS_STACK"][:4]

for group in placements.values():
    for item in group:
        print(item)

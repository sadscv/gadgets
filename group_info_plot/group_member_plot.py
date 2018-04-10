import csv

import matplotlib.pyplot as plt
import pandas
import seaborn

# airports = pandas.read_csv("airports.csv", header=None, dtype=str)

output = []

idx_line = 0
with open ('test_data.csv') as f:
    for line in f:
        idx_line += 1
        line_splits = line.strip().split(' ')
        print(line_splits)
        line_formated = [line_splits[0], 0, 0]
        for s in line_splits:
            if str(s).strip() == 'm':
                line_formated[1] += 1
            elif str(s).strip() == 'f':
                line_formated[2] += 1
        output.append(line_formated)

with open('data_output.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerows(output)

data = pandas.read_csv('data_output.csv',  header=None, dtype=int)
data.head(10)
data.columns('test')
seaborn.distplot()
seaborn.his

plt.hist(data, bins=2)


import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
from collections import defaultdict
import numpy as np
import os
import csv
import preprocess

FILE_PATH = 'PROCESSED_DATA/COMBINED_CSVs/'
TIME_STEP = 0.25


# main
def main():
    characters = list()
    lengths = list()
    notes = list()
    counts = {}
    length = 0

    for root, dirs, files in os.walk(FILE_PATH, topdown=False):
        for name in files:

            # go through file dataset and plot the lengths
            df = pd.read_csv(os.path.join(FILE_PATH, name))

            for index, row in df.iterrows():
                length = round(row['length'], 3)
                # note = row['note']
                note = preprocess.transpose(row, name)

                # print(length)
                # make sure it's not too large
                if length < 50:
                    notes.append(note)
                    lengths.append(length)
                    # add it to the counter dictionary
                    if length in counts:
                        counts[length] += 1
                    else:
                        counts[length] = 1
    print(counts)

    # display the results
    x = list(counts.keys())
    y = list(counts.values())
    plt.scatter(notes, lengths, color='navy')

    plt.xlabel("Notes")
    plt.ylabel("Lengths")
    plt.title("Occurences of Given Lengths in Rock Corpus Dataset")
    # plt.show()

    print(len(counts))
    # 398
    print(len(set(notes)))
    # 31
    print(sum(counts.values()))
    # 59185


if __name__ == "__main__":
    main()

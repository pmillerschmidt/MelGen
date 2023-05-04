import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
from collections import defaultdict
import numpy as np
import os
import csv
# import preprocess

FILE_PATH = 'PROCESSED_DATA/COMBINED_CSVs/'
TIME_STEP = 0.25


# main
def main():
    characters = list()
    lengths = list()
    notes = list()
    counts = {}
    length = 0

    # for root, dirs, files in os.walk(FILE_PATH, topdown=False):
    #     for name in files:

    #         # go through file dataset and plot the lengths
    #         df = pd.read_csv(os.path.join(FILE_PATH, name))

    #         for index, row in df.iterrows():
    #             length = round(row['length'], 3)
    #             # note = row['note']
    #             note = preprocess.transpose(row, name)

    #             # print(length)
    #             # make sure it's not too large
    #             if length < 50:
    #                 notes.append(note)
    #                 lengths.append(length)
    #                 # add it to the counter dictionary
    #                 if length in counts:
    #                     counts[length] += 1
    #                 else:
    #                     counts[length] = 1
    # print(counts)

    x = [i for i in range(50)]

    # display the results
    loss = [0.99, 0.81, 0.77, 0.74, 0.71,
            0.69, 0.66, 0.64, 0.63, 0.61,
            0.59, 0.54, 0.53, 0.51, 0.49,
            0.48, 0.46, 0.45, 0.44, 0.43,
            0.41, 0.41, 0.40, 0.4, 0.38,
            0.37, 0.37, 0.36, 0.35, 0.35,
            0.34, 0.34, 0.33, 0.33, 0.32,
            0.32, 0.32, 0.31, 0.31, 0.30,
            0.30, 0.30, 0.29, 0.29, 0.29,
            0.28, 0.28, 0.27, 0.27, 0.27]

    accuracy = [0.77, 0.78, 0.78, 0.79, 0.79,
                0.80, 0.81, 0.81, 0.81, 0.82,
                0.83, 0.83, 0.84, 0.84, 0.85,
                0.85, 0.85, 0.86, 0.86, 0.87,
                0.87, 0.87, 0.87, 0.87, 0.88,
                0.88, 0.88, 0.89, 0.89, 0.89,
                0.89, 0.89, 0.89, 0.9, 0.9,
                0.9, 0.9, 0.9, 0.9, 0.9,
                0.91, 0.91, 0.91, 0.91, 0.91,
                0.91, 0.91, 0.91, 0.915, 0.915]

    plt.plot(x, loss, label="loss", color='navy')
    plt.plot(x, accuracy, label="accuracy", color='maroon')
    plt.title('Loss and Accuracy of MelGen')
    plt.xlabel('Epochs')
    plt.ylabel('Loss/Accuracy')

    plt.legend()
    plt.show()
    # plt.scatter(loss, accuracy, color='navy')

    # plt.xlabel("Notes")
    # plt.ylabel("Lengths")
    # plt.title("Occurences of Given Lengths in Rock Corpus Dataset")
    # # plt.show()

    print(x)


if __name__ == "__main__":
    main()

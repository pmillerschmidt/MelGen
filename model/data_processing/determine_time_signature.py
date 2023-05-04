import os
import music21 as m21
import pandas as pd
import csv
from csv import writer
from csv import reader

CSV_PATH = "PROCESSED_DATA/COMBINED_CSVs"


def determine_mode(data_path):
    lengths = list()
    df = pd.read_csv(data_path)
    for i, row in df.iterrows():
        lengths.append(row['length'])

    lengths = set(lengths)
    print("SONG: " + str(data_path))
    print(lengths)


def main():
    matches = 0

    # walk through chords
    for root, dirs, files in os.walk(CSV_PATH, topdown=False):

        for name in files:
            determine_mode(os.path.join(CSV_PATH, name))


if __name__ == "__main__":
    main()

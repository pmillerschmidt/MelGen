import os
import music21 as m21
import csv
from csv import writer


FILE_PATH = "PROCESSED_DATA/MELODIES/a_day_in_the_life_tdc.txt"
FILE_NAME = "a_day_in_the_life_tdc.txt"


def main():
    # open file and get lines
    f = open(FILE_PATH, "r")
    lines = f.readlines()

    # open csv
    csv_name = FILE_PATH.split(".")[0] + ".csv"
    csv = open(csv_name, "w")
    writer_obj = writer(csv)

    for line in lines:
        contents = list(line.rstrip('\n').split())
        writer_obj.writerow(contents)


if __name__ == "__main__":
    main()

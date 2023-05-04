import os
import music21 as m21
import csv
from csv import writer


FILE_PATH = "PROCESSED_DATA/CHORDS/"
# FILE_NAME = "a_day_in_the_life_tdc.txt"


# write csv file from file name

def write_csv(file_path):
    # open file and get lines
    f = open(file_path, "r")
    lines = f.readlines()

    # open csv
    csv_name = file_path.split(".")[0] + ".csv"
    csv = open(csv_name, "w")
    writer_obj = writer(csv)

    # adding header
    headerList = ['start', 'end', 'numeral', 'chromatic root',
                  'diatonic root', 'key', 'absolute root']

    # converting data frame to csv
    writer_obj.writerow(headerList)

    # go through all the notes, adding them and their
    for line in lines[1:-2]:

        contents = list(line.rstrip('\n').split())
        writer_obj.writerow(contents)


def main():

    for root, dirs, files in os.walk(FILE_PATH, topdown=False):
        for name in files:

            if name != ".DS_Store" and name.split(".")[1] == "txt":
                print(name)
                write_csv(os.path.join(root, name))


if __name__ == "__main__":
    main()

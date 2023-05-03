import os
import music21 as m21
import csv
from csv import writer


FILE_PATH = "../PROCESSED_DATA/MELODIES/"
# FILE_NAME = "a_day_in_the_life_tdc.txt"


# write csv file from file name

def write_csv(file_path, name):
    # open file and get lines
    f = open(file_path, "r")
    lines = f.readlines()

    # open csv
    csv_name = name.split(".")[0] + ".csv"
    csv = open(csv_name, "w")
    writer_obj = writer(csv)

    # adding header
    headerList = ['time', 'note', 'scale degree', 'length']

    # converting data frame to csv
    writer_obj.writerow(headerList)

    # start with getting the first note and its time
    curr_note = list(lines[0].rstrip('\n').split())
    prev_time = curr_note[0]

    # go through all the notes, adding them and their
    for line in lines[1:]:

        contents = list(line.rstrip('\n').split())
        length = float(contents[0]) - float(prev_time)
        prev_time = contents[0]
        # contents.append(length)
        curr_note.append(length)
        writer_obj.writerow(curr_note)
        curr_note = contents


def main():

    for root, dirs, files in os.walk(FILE_PATH, topdown=False):
        for name in files:

            if name != ".DS_Store" and name.split(".")[1] == "txt":
                print(name)
                write_csv(os.path.join(root, name), name)


if __name__ == "__main__":
    main()

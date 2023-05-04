import os
import music21 as m21
import pandas as pd
import csv
from csv import writer
from csv import reader

CHORD_PATH = "../PROCESSED_DATA/CHORD_CSVs/"
MELODY_PATH = "../PROCESSED_DATA/MELODY_CSVs/"
CSV_PATH = "../PROCESSED_DATA/COMBINED_CSVs"


def create_combined_csv(chord_path, melody_path, song_name):
    # print song name
    # print(song_name)

    # get chord csv as data frame
    chord_df = pd.read_csv(chord_path)
    chord_columns = list(chord_df.columns)

    # get melody csv as data frame
    melody_df = pd.read_csv(melody_path)
    melody_columns = list(melody_df.columns)

    # create combined df
    combined_df = pd.DataFrame(columns=['time', 'note', 'scale degree', 'length', 'start',
                               'end', 'numeral', 'chromatic root', 'diatonic root', 'key', 'absolute root'])

    for i, mel_row in melody_df.iterrows():
        # get the time
        time = float(mel_row['time'])
        # see what chord is playing at that time
        for j, chord_row in chord_df.iterrows():

            start = float(chord_row['start'])
            end = float(chord_row['end'])

            # if the note time is before the start of the chord, break
            if time < start:
                continue

            # if the note is in the start/end time, add it
            elif time >= start and time <= end:
                # print("MATCH")
                # print("----------")
                # print(mel_row)
                # print(chord_row)
                # add the values
                combined_df.loc[len(combined_df.index)] = [
                    mel_row['time'], mel_row['note'], mel_row['scale degree'], mel_row['length'], chord_row[
                        'start'], chord_row['end'], chord_row['numeral'], chord_row['chromatic root'],
                    chord_row['diatonic root'], chord_row['key'], chord_row['absolute root']]
                # exit so multiple notes aren't counted
                break

    # print(combined_df)

    # add the dataframe to a csv
    # # open the new csv
    csv_name = "COMBINED_" + song_name + ".csv"
    csv = open(csv_name, "w")
    # writer_obj = writer(csv)
    combined_df.to_csv(csv_name)

    # with open(chord_path) as chord_csv:
    #     read = csv.reader(chord_csv, delimiter=',')

    #     # get header
    #     header = []
    #     header = next(read)
    #     print(header)

    # for row in read:
    #     print(row)


def main():
    matches = 0

    # walk through chords
    for root, dirs, files in os.walk(CHORD_PATH, topdown=False):

        for name in files:

            chord_song_name = name.split(".")[0]
            # print("CHORD NAME: " + chord_song_name)
            # search through melodies for a match
            for root, dirs, files in os.walk(MELODY_PATH, topdown=False):
                for name in files:

                    melody_song_name = name.split(".")[0]

                    if chord_song_name == melody_song_name:
                        # print(melody_song_name)
                        create_combined_csv(os.path.join(
                            CHORD_PATH, chord_song_name + ".csv"), os.path.join(MELODY_PATH, melody_song_name + ".csv"), chord_song_name)


if __name__ == "__main__":
    main()

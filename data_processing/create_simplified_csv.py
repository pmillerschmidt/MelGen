import os
import music21 as m21
import pandas as pd
import csv
from csv import writer
from csv import reader

from preprocess import quantize, find_nearest, ACCEPTABLE_LENGTHS, ACCEPTABLE_NOTES, MAJOR_NUMERALS, MINOR_NUMERALS

CHORD_PATH = "../PROCESSED_DATA/CHORD_CSVs/"
MELODY_PATH = "../PROCESSED_DATA/MELODY_CSVs/"
CSV_PATH = "../PROCESSED_DATA/COMBINED_CSVs"

# transpose a note


def transpose(note, numeral, key, song):
    # get the important data

    # major --> C major, minor --> A minor
    if numeral in MAJOR_NUMERALS:
        new_note = note - key

    elif numeral in MINOR_NUMERALS:
        new_note = note - key - 3

    # major it in the scale
    new_note = find_nearest(ACCEPTABLE_NOTES, new_note)

    # make it within this two octave range
    return int(new_note)


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
    simplified_df = pd.DataFrame(columns=['note', 'length', 'diatonic root'])

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

                # add the values
                note = transpose(
                    mel_row['note'], chord_row['numeral'], chord_row['key'], song_name)
                length = quantize(mel_row['length'], ACCEPTABLE_LENGTHS)
                simplified_df.loc[len(simplified_df.index)] = [
                    note, length, chord_row['diatonic root']]
                # exit so multiple notes aren't counted
                break

    # print(combined_df)

    # add the dataframe to a csv
    # # open the new csv
    csv_name = "SIMPLIFIED_" + song_name + ".csv"
    csv = open(csv_name, "w")
    # writer_obj = writer(csv)
    simplified_df.to_csv(csv_name)


def main():
    matches = 0

    # walk through chords
    for root, dirs, files in os.walk(CHORD_PATH, topdown=False):

        for name in files:

            chord_song_name = name.split(".")[0]

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

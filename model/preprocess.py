import os
import music21 as m21
import json
import tensorflow.keras as keras
import numpy as np
import pandas as pd
import math

DATASET_PATH = "PROCESSED_DATA/COMBINED_CSVs"
SAVE_DIR = "preprocessed_chord_set"
SINGLE_FILE_DATASET = "file_dataset"
SEQUENCE_LENGTH = 64
MAPPING_PATH = "model/mappings.json"
TIME_STEP = 0.0625


# acceptable durations, notes get more sparse as they get longer
# REMOVED 0.0625
ACCEPTABLE_LENGTHS = [0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875,
                      1, 1.125, 1.5, 1.625, 1.75, 1.875, 2, 2.25, 2.5, 2.75, 3, 3.5, 4]

MAJOR_NUMERALS = {'I', 'ii', 'iii', 'IV', 'V', 'vi', 'vii', 'V7/IV', 'V/vi', 'vih7', 'bV', 'vi64', 'V6/ii', 'V43/IV',
                  'V7/V', 'Vs4', 'V7', 'IV7', 'IVd43', 'ii6', 'V64', 'ii7/vi', 'V6/vi', 'ii65', 'iih7/vi', 'iv6/ii', 'viix7/ii',
                  'V11', 'V6', 'ii7', 'V43', 'IV6', 'vi7', 'V/ii', 'iih43/ii', 'V42/IV', 'iih7/V', 'biii', 'iii64', 'V7/I', 'iii7',
                  'bVb5', 'viix7/V', 'V/V', 'V7/vi', 'Id7', 'V7/iii', 'V42', 'viix42', 'iih43', 'bvi', 'bvii7', 'iih7', 'V65/IV', 'IVd7',
                  'I6', 'vi6', 'viix42/V', 'viih7/V', 'V/IV', 'I64', 'viix7/vi', 'V65/V', 'ii/IV', 'iih65', 'IV/IV', 'V6/V', 'V65/vi',
                  'IV64', 'I7', 'V7/ii'

                  }
MINOR_NUMERALS = {'i', 'ii*', 'III', 'iv', 'v', 'VI', 'VII', 'v65', 'bIII6', 'bVId7', 'II', 'bIII7', 'iv65', 'III64', 'bVII6',
                  'bIIId7', 'iih65/ii', 'i7', 'bVIb5', 'iii6',  'v11', 'bVI', 'V/bVI', 'bIII64', 'bIII', 'V7/II', 'bII7', 'bVII64',
                  'iv7', 'i42', 'V/VII', 'bVI7', 'iio6', 'bVIId7', 'i6', 'iio', 'v7', 'bVII', 'bVI6', 'V7/III'

                  }
UNKNOWN_NUMERALS = set()
NOTES = set()
NOTE_COUNTS = {}

# # major scale
# MAJOR_SCALE = [0, 2, 4, 5, 7, 9, 11]
# # generate c major scale
# ACCEPTABLE_NOTES = []
# for i in range(2, 7):
#     ACCEPTABLE_NOTES.extend([x + 12*i for x in MAJOR_SCALE])

# C major scale from c-2 to c3
ACCEPTABLE_NOTES = [24, 26, 28, 29, 31, 33, 35, 36, 38, 40, 41, 43, 45, 47, 48,
                    50, 52, 53, 55, 57, 59, 60, 62, 64, 65, 67, 69, 71, 72, 74, 76, 77, 79, 81, 83]


def load_songs(dataset_path):

    songs = []

    # go through all the files in dataset and load
    for path, subdir, files in os.walk(dataset_path):
        for file in files:
            if file[-3:] == "csv":
                songs.append(file)
    return songs


# find nearest value in an array
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

# quantize a note


def quantize(length, acceptable_lengths):
    return find_nearest(acceptable_lengths, length)


# normalize a note to be within a range
def normalize(low, high, note):
    # if its below or above the range, make it within range
    if note < low:
        note += 12
        return normalize(low, high, note)
    elif note >= high:
        note -= 12
        return normalize(low, high, note)

    return note


def transpose(row, song):
    # get the important data
    numeral = row['numeral']
    original_note = row['note']
    key = row['key']

    # major --> C major, minor --> A minor
    if numeral in MAJOR_NUMERALS:
        new_note = original_note - key

    elif numeral in MINOR_NUMERALS:
        new_note = original_note - key - 3

    else:
        UNKNOWN_NUMERALS.add(numeral)

    # major it in the scale
    new_note = find_nearest(ACCEPTABLE_NOTES, new_note)

    # tally the new note
    if new_note in NOTE_COUNTS:
        NOTE_COUNTS[new_note] += 1
    else:
        NOTE_COUNTS[new_note] = 1

    # if new_note not in ACCEPTABLE_NOTES:
    #     print("SONG: " + str(song))
    #     print("NOTE: " + str(original_note))
    #     print("NEW NOTE: " + str(new_note))
    #     print("NUMERAL: " + str(numeral))
    #     print("CHORD: " + str(row['diatonic root']))
    #     print("KEY: " + str(row['key']))
    #     print("------")

    # make it within this two octave range
    return normalize(48, 72, int(new_note))
    # return int(new_note)

    # default time step to a sixteenth note

    # THIS IS A LITTLE IMPRECISE

    # time step is 1/16th notes


def encode_song(song, time_step=TIME_STEP):
    encoded_song = []

    df = pd.read_csv(os.path.join(DATASET_PATH, song))
    simplified_df = pd.DataFrame(columns=['note', 'length', 'root'])

    for i, row in df.iterrows():

        chord = row['diatonic root']
        # transpose the note
        note = transpose(row, song)
        NOTES.add(note)

        # quantize note
        length = row['length']
        length = quantize(length, ACCEPTABLE_LENGTHS)

        # convert notes to time series representation
        steps = int(length / time_step)

        for step in range(steps):
            if step == 0:
                # just note
                # encoded_song.append(str(note))
                # with chord
                encoded_song.append(str(note) + "_" + str(chord))
            else:
                encoded_song.append("_")

    # # save to csv
    # csv_name = "SIMPLIFIED_" + song + ".csv"
    # csv = open(csv_name, "w")

    # simplified_df.loc[len(simplified_df.index)] = [note, length, chord]
    # # writer_obj = writer(csv)
    # simplified_df.to_csv(csv_name)

    # cast encoded song to a str
    encoded_song = " ".join(map(str, encoded_song))

    return encoded_song


def preprocess(dataset_path):

    # load the songs
    print("Loading songs...")
    songs = load_songs(dataset_path)
    print(f"Loaded {len(songs)} songs.")

    # iterate through songs and encode them
    for i, song in enumerate(songs):

        # encode songs with music time series representation -> get str encoding
        encoded_song = encode_song(song)

        # save songs to text file
        save_path = os.path.join(SAVE_DIR, str(i))
        with open(save_path, "w") as fp:
            fp.write(encoded_song)


# load a song file from a path
def load(file_path):
    with open(file_path, "r") as fp:
        song = fp.read()
    return song


def create_single_file_dataset(dataset_path, file_dataset_path, sequence_length):
    new_song_delimiter = "/ " * sequence_length
    songs = ""

    # load encoded songs and add delimiters
    for path, _, files in os.walk(dataset_path):
        for file in files:
            file_path = os.path.join(path, file)
            song = load(file_path)
            songs = songs + song + " " + new_song_delimiter

    songs = songs[:-1]

    # save string that contains all dataset
    with open(file_dataset_path, "w") as fp:
        fp.write(songs)

    return songs


def create_mapping(songs, mapping_path):
    mappings = {}

    # identify the vocabulary
    songs = songs.split()
    vocabulary = list(set(songs))
    # print(vocabulary)

    # create mappings look-up table
    for i, symbol in enumerate(vocabulary):
        mappings[symbol] = i

    # save vocabulary to a json file
    with open(mapping_path, "w") as fp:
        json.dump(mappings, fp, indent=4)


def convert_songs_to_int(songs):
    int_songs = []

    # load mappings
    with open(MAPPING_PATH, "r") as fp:
        mappings = json.load(fp)

    # cast songs string to a list
    songs = songs.split()

    # map songs to int
    for symbol in songs:
        int_songs.append(mappings[symbol])

    return int_songs


def generate_training_sequences(sequence_length):
    # load songs and map them to int
    songs = load(SINGLE_FILE_DATASET)
    int_songs = convert_songs_to_int(songs)

    # generate the training sequences
    inputs = []
    targets = []

    num_sequences = len(int_songs) - sequence_length
    for i in range(num_sequences):
        inputs.append(int_songs[i:i+sequence_length])
        targets.append(int_songs[i+sequence_length])

    # one-hot encode the sequences
    # one-hot encoding creates a list where the elements are lists
    # of the size of the vocabulary and are all zero except for the
    # one value in the vocab that is true (1)

    # inputs: (# of sequences, sequence length, vocabulary size)
    # [ [0, 1, 2], [1, 1, 2] ] --> [ [1, 0, 0], [0, 1, 0], [0, 0, 1], [] ]
    vocab_size = len(set(int_songs))
    inputs = keras.utils.to_categorical(inputs, num_classes=vocab_size)
    targets = np.array(targets)

    return inputs, targets


def main():

    preprocess(DATASET_PATH)
    # print(NOTE_COUNTS)
    songs = create_single_file_dataset(
        SAVE_DIR, SINGLE_FILE_DATASET, SEQUENCE_LENGTH)
    create_mapping(songs, MAPPING_PATH)

    inputs, targets = generate_training_sequences(SEQUENCE_LENGTH)


if __name__ == "__main__":
    main()

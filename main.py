import sys
import os
import tensorflow as tf
from tensorflow import keras
# from tensorflow.keras import Model
import numpy as np
import json
import music21 as m21
from music21 import converter, corpus, instrument, midi, note, chord, pitch
from model.preprocess import SEQUENCE_LENGTH, MAPPING_PATH
import model.generator as gen

TIME_STEP = 0.25
chord_dict = {36: 1, 38: 2, 40: 3, 41: 4, 43: 5, 45: 6, 47: 7,
              48: 1, 50: 2, 52: 3, 53: 4, 55: 5, 57: 6, 58: 7,
              60: 1, 62: 2, 64: 3, 65: 4, 67: 5, 69: 6, 71: 7,
              72: 1, 74: 2, 76: 3, 77: 4, 79: 5, 81: 6, 83: 7}

# extract notes


def extract_notes(midi_part):
    notes = []

    # iterate through the notes
    for nt in midi_part.flat.notes:
        # if its a note
        if isinstance(nt, note.Note):
            pitch = nt.pitch.ps
            duration = float(nt.duration.quarterLength)
            notes.append((pitch, duration))

    return notes


# get chord progression

def get_cp(chord_file):
    out = []
    curr_time = 0
    cf = m21.converter.parse(os.path.join('.', chord_file))
    parts = cf.getElementsByClass(m21.stream.Part)
    cp_notes = extract_notes(parts[0])

    for note in cp_notes:
        curr_time += note[1]
        out.append((chord_dict[int(note[0])], int(curr_time)))

    return out


#  get seed


def get_seed(seed_file, cp):

    out = ""
    seed = m21.converter.parse(os.path.join('.', seed_file))
    parts = seed.getElementsByClass(m21.stream.Part)
    seed_notes = extract_notes(parts[0])
    init_chord = cp[0][0]

    for note in seed_notes:
        time_remaining = note[1]
        # add the note
        out += str(int(note[0])) + "_" + str(init_chord) + " "
        # add the continuations
        while time_remaining > 0:
            out += "_ "
            time_remaining -= TIME_STEP
    return out


def main():

    # read in arguments
    if len(sys.argv) != 3:
        print("NOT ENOUGH ARGUMENTS. ENTER A CHORD MIDI AND A SEED MELODY MIDI.")
        return -1

    # get the cp and seed melody
    cp = get_cp(sys.argv[2])
    seed = get_seed(sys.argv[1], cp)

    # make the melody generator
    mg = gen.MelodyGenerator()

    melody = mg.generate_melody(seed, 256, SEQUENCE_LENGTH, 0.7, cp)
    print(melody)
    mg.save_melody(melody, cp)


if __name__ == "__main__":
    main()

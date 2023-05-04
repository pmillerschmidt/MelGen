import os
import music21 as m21
from midiutil.MidiFile import MIDIFile

FILE_PATH = "PROCESSED_DATA/MELODIES/a_day_in_the_life_tdc.txt"


def main():
    # open file and get lines
    f = open(FILE_PATH, "r")
    lines = f.readlines()

    # create your MIDI object
    mf = MIDIFile(1)     # only 1 track
    track = 0   # the only track

    time = 0    # start at the beginning
    mf.addTrackName(track, time, "Sample Track")
    mf.addTempo(track, time, 120)

    # add some notes
    channel = 0
    volume = 100

    for line in lines:
        data = line.split()
        pitch = int(data[1])
        time = float(data[0])
        print("time: " + str(time))
        mf.addNote(track, channel, pitch, time, 0.5, volume)

    # write it to disk
    with open("output.mid", 'wb') as outf:
        mf.writeFile(outf)


if __name__ == "__main__":
    main()

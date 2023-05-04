import tensorflow as tf
from tensorflow import keras
# from tensorflow.keras import Model
import numpy as np
import json
import music21 as m21
from .preprocess import SEQUENCE_LENGTH, MAPPING_PATH


TIME_STEP = 0.25

chord_dict = {1: 60, 2: 62, 3: 64, 4: 65, 5: 67, 6: 69, 7: 71}


class MelodyGenerator:

    def __init__(self, model_path="model/CHORD_LSTM-model.h5"):

        self.model_path = model_path
        self.model = tf.keras.models.load_model(model_path)
        self.root = None

        # hyper-parameters (continuation, variance)

        self.baseline_continuation_reduction = 1.3
        self.continuation_reduction = self.baseline_continuation_reduction
        self.continuation_multiplier = 1.4

        with open(MAPPING_PATH, "r") as fp:
            self._mappings = json.load(fp)

        self._start_symbols = ["/"] * SEQUENCE_LENGTH

    def generate_melody(self, seed, num_steps, max_sequence_length, temperature, cp):

        # create seed with start symbols
        seed = seed.split()
        melody = seed
        seed = self._start_symbols + seed

        # time and intial root
        time = 0

        curr_chord = 0
        self.root = cp[curr_chord][0]

        # map seed to int
        seed = [self._mappings[symbol] for symbol in seed]

        for _ in range(num_steps):

            # get the chord
            self.root = cp[curr_chord][0]

            # limit the seed to max_sequence_length
            seed = seed[-max_sequence_length:]

            # one-hot encode the seed
            onehot_seed = keras.utils.to_categorical(
                seed, num_classes=len(self._mappings))
            # (1, max_sequence_length, num of symbols in the vocabulary)

            # convert bidirectional array into 3D array
            onehot_seed = onehot_seed[np.newaxis, ...]
            # make a prediction
            probabilities = self.model.predict(onehot_seed)[0]
            # print(probabilities)

            # get the sampled output
            output = self._sample_with_temperature(
                probabilities, temperature)
            new_seed = output[0]
            output_symbol = output[1]
            # check whether we are at the end of a melody
            if output_symbol == "/":
                break

            # increment time
            time += TIME_STEP

            # if its the next chord, change the root
            if time >= cp[curr_chord][1]:
                curr_chord += 1
                # if the chord changes and its not a continuation, change the seed
                # if output_symbol != "_":
                #     new_seed = self._mappings[output_symbol[0:2] +
                #                               "_" + str(cp[curr_chord][0])]

                # if its out of range, break
                if curr_chord >= len(cp):
                    return melody

            # update seed
            seed.append(new_seed)

            # update melody
            melody.append(output_symbol)

        return melody

    def get_options(self, choices):
        options = []
        for choice in choices:
            value = list(
                {i for i in self._mappings if self._mappings[i] == choice})[0]
            options.append(value)
        return options

    # if the note can be chosen based on the current chord
    def get_chord_options(self, option):
        # print(option[0].split('_')[1])
        if option[0] == '_' or option[0] == '/':
            return True
        elif int(option[0].split('_')[1]) == self.root:
            return True
        return False

    # normalize probabilities to 1
    def normalize_probabilites(self, probs):
        prob_factor = 1 / sum(probs)
        return [prob_factor * p for p in probs]

    def reduce_continuation(self, option_probs):
        # reduce continuation probability
        for i, option in enumerate(option_probs):
            if option[0] == '_':
                prob = option[1] / self.continuation_reduction
                option_probs.pop(i)
                option_probs.append(('_', prob))
        return option_probs

    def _sample_with_temperature(self, probabilities, temperature):

        # temperature -> infinity
        # temperature -> 0
        # temperature = 1
        # higher temperature means more unpredictable sampling

        # get a smaller distribution dependent on temperature
        predictions = np.log(probabilities) / temperature

        # apply softmax, get more homogenous distribution
        probabilities = np.exp(predictions) / np.sum(np.exp(predictions))

        choices = range(len(probabilities))
        options = self.get_options(choices)

        # filter out the options
        option_probs = list(zip(options, probabilities))
        option_probs = list(
            filter(self.get_chord_options, option_probs))

        # reduce the continuation probability
        option_probs = self.reduce_continuation(option_probs)

        # get the potential probabilities
        filtered_options = [prob[0] for prob in option_probs]
        filtered_probalities = self.normalize_probabilites(
            [prob[1] for prob in option_probs])

        note = np.random.choice(
            filtered_options, p=filtered_probalities)

        # if its a continuation, increase the continuation reduction
        if note == "_":
            self.continuation_reduction *= self.continuation_multiplier
        # otherwise, reset continuation reduction
        else:
            self.continuation_reduction = self.baseline_continuation_reduction

        output_int = self._mappings[note]

        return output_int, note

        # print(list(zip(choices, probabilities)))

        # for each item of choices we have a given probability
        # index = np.random.choice(choices, p=probabilities)

        # return index

    def save_melody(self, melody, cp, step_duration=TIME_STEP, format="midi", file_name="mel.mid"):

        # create a music21 stream
        stream = m21.stream.Stream()

        # overall time
        time = 0

        # parse all the symbols in the melody and create note/rest objects
        start_symbol = None
        step_counter = 1

        for i, symbol in enumerate(melody):

            # handle case in which we have a note/rest or the melody is over
            if symbol != "_" or i + 1 == len(melody):

                # ensure we're dealing with a note/rest
                if start_symbol is not None:

                    quarter_length_duration = step_duration * step_counter

                    # handle note
                    m21_event = m21.note.Note(
                        int(start_symbol[0:2]),
                        quarterLength=quarter_length_duration)

                    stream.append(m21_event)

                    # reset step counter
                    step_counter = 1

                start_symbol = symbol

            # handle case in which we have a prolongation
            else:
                step_counter += 1

        # # add chord progression
        # for chord in cp:
        #     # handle note
        #     m21_event = m21.note.Note(
        #         chord_dict[int(chord[0])],
        #         quarterLength=chord[1])

        #     stream.append(m21_event)

        # write the m21 stream to a midi file
        stream.write(format, file_name)


if __name__ == "__main__":

    mg = MelodyGenerator()

    # underlying chord progression

    cp = [(1, 4), (6, 8), (4, 12), (5, 16), (1, 20), (6, 24), (4, 28), (5, 32)]

    seed = "60_1 _ _ _ 67_1 _ _ _"

    melody = mg.generate_melody(seed, 256, SEQUENCE_LENGTH, 0.7, cp)
    print(melody)
    mg.save_melody(melody, cp)

# import tensorflow.python.keras as keras
from tensorflow import keras
from preprocess import generate_training_sequences, SEQUENCE_LENGTH


# number of elements in vocab
OUTPUT_UNITS = 99
NUM_UNITS = [256]
LOSS = "sparse_categorical_crossentropy"
LEARNING_RATE = 0.001
EPOCHS = 50
BATCH_SIZE = 64
SAVE_MODEL_PATH = "CHORD_LSTM-model.h5"


def build_model(output_units, num_units, loss, learning_rate):
    # create the model architrecture
    input = keras.layers.Input(shape=(None, output_units))
    # drawing an arrow from input to the LSTM layer
    x = keras.layers.LSTM(num_units[0])(input)
    # add a dropout layer - prevents overfitting
    x = keras.layers.Dropout(0.3)(x)

    # output layer -> softmax classifier
    output = keras.layers.Dense(output_units, activation="softmax")(x)

    # build the model
    model = keras.Model(input, output)

    # compile model
    model.compile(loss=loss,
                  optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
                  metrics=["accuracy"])

    return model


def train(output_units=OUTPUT_UNITS, num_units=NUM_UNITS, loss=LOSS, learning_rate=LEARNING_RATE):

    # generate the training sequences
    inputs, targets = generate_training_sequences(SEQUENCE_LENGTH)

    # build the network
    model = build_model(output_units, num_units, loss, learning_rate)

    # train the model
    model.fit(inputs, targets, epochs=EPOCHS, batch_size=BATCH_SIZE)

    # save the model
    model.save(SAVE_MODEL_PATH)


if __name__ == "__main__":
    train()

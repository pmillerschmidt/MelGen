






# MelGen: Applying LSTMs to Melody Generation

https://github.com/user-attachments/assets/ef22f6e9-db83-4c10-b93a-eb18ea056743

### Abstract

Machine Learning models have already changed the way we think about and interact with text, images, and video. The implementation of Transformers in Generative Pre-Trained Models, such as ChatGPT and Dall-E, has shown how powerful these technologies can be. However, music generation presents a unique challenge. When sampled at 44100hz, a 25-second clip of audio has more than a million data points. In addition, music has complex temporal structures and hierarchical patterns. Multiple instruments are dependent on each other in nuanced ways and identifying commonalities and patterns is challenging. When building a generative musical model, a decision must be made between generating simpler representations or pure audio. Previous works have used basic model architectures, such as RNNs and LSTMs, for MIDI or XML generation and more complicated architectures, such as GANs and VQ-VAEs, for pure audio generation. This paper investigates the existing research and outlines the development of MelGen, an artificially intelligent MIDI generator. The model was trained on the Rock Corpus Dataset [1], a collection of harmonic analyses and melodic transcriptions of popular songs from the 20th century. The LSTM was trained for over 24 hours with a learning rate of 0.001, using sparse categorical cross-entropy for loss. Due to the size of the dataset and the specificity of the task (attention to harmonic structure), the raw data generated by the model had serious inconsistencies. Specifically, due to filtering out non-chord choices, the likelihood of a continuation was overestimated, meaning that the generated MIDI would get “stuck” on notes for a long time. To account for this, I implemented continuation reduction to decrease the likelihood of continuations depending on the current note length. This had the effect of generating more consistent and reasonable melodies. 

### Interaction

To run the generator, drag a MIDI file of chords and a MIDI file seed melody into the same folder as the generator. Then call python3 generator.py [MIDI FILE] [SEED MELODY FILE]. The generated melody will appear in the folder titled 'mel.mid'. 

### Code Overview

The folder data_processing contains all of the python files used to clean the data from the Rock Corpus dataset and turn it into usable data, in the form of the file_dataset used for training. 

For training, I used Tensorflow and Keras to build an LSTM model with one LSTM layer, a Dropout layer, and a softmax classifier. The Model was then trained over 50 epochs using Sparse Categorical Cross-Entropy for loss, a learning rate of 0.001, a batch size of 64, and Keras’ optimizer Adam. The module used for training is train.py, and can be called to train the model based on the data processed in file_dataset. 

The Generator is in generator.py and is fed a seed sequence of chord degrees (with time offsets) and a seed melody to build on. It then generated melody MIDI data with a 1/8th note time step.


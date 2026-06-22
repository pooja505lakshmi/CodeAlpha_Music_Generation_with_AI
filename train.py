from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.utils import to_categorical
import numpy as np

with open("notes.txt", "r") as f:
    notes = [line.strip() for line in f]

unique_notes = sorted(set(notes))

note_to_int = dict((note, number) for number, note in enumerate(unique_notes))

sequence_length = 50

network_input = []
network_output = []

for i in range(len(notes) - sequence_length):
    seq_in = notes[i:i + sequence_length]
    seq_out = notes[i + sequence_length]

    network_input.append([note_to_int[n] for n in seq_in])
    network_output.append(note_to_int[seq_out])

n_patterns = len(network_input)

network_input = np.reshape(
    network_input, (n_patterns, sequence_length, 1)
)

network_input = network_input / float(len(unique_notes))

network_output = to_categorical(network_output)

model = Sequential()

model.add(LSTM(
    256,
    return_sequences=True,
    input_shape=(network_input.shape[1], network_input.shape[2])
))
model.add(Dropout(0.3))

model.add(LSTM(256))
model.add(Dropout(0.3))

model.add(Dense(network_output.shape[1], activation='softmax'))
model.compile(
    loss='categorical_crossentropy',
    optimizer='adam'
)

model.fit(
    network_input,
    network_output,
    epochs=100,
    batch_size=64
)

model.save("music_model.keras")

print("Model saved!")
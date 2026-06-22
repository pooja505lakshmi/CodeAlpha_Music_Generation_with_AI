print("STEP 1: Script started")

from music21 import stream, note, chord
import numpy as np
import random
from tensorflow.keras.models import load_model

print("STEP 2: Loading model...")

model = load_model("music_model.keras")

print("STEP 3: Model loaded")

with open("notes.txt", "r") as f:
    notes = [line.strip() for line in f]

print("STEP 4: Notes loaded =", len(notes))

pitchnames = sorted(set(notes))
note_to_int = {n: i for i, n in enumerate(pitchnames)}
int_to_note = {i: n for i, n in enumerate(pitchnames)}

sequence_length = 50

start = random.randint(0, len(notes) - sequence_length)
pattern = notes[start:start + sequence_length]

output_notes = []

print("STEP 5: Starting generation loop")

for i in range(300):  # reduced for debugging
    input_seq = [note_to_int[n] for n in pattern]
    input_seq = np.reshape(input_seq, (1, sequence_length, 1))
    input_seq = input_seq / float(len(pitchnames))

    prediction = model.predict(input_seq, verbose=0)
    index = np.argmax(prediction)

    result = int_to_note[index]

    output_notes.append(result)

    pattern.append(result)
    pattern = pattern[1:]

print("STEP 6: Generation complete")

offset = 0
output_stream = stream.Stream()

for item in output_notes:

    # Skip invalid values like "0", "1", etc.
    if item.isdigit():
        print("Skipped invalid note:", item)
        continue

    try:
        if "." in item:
            c = chord.Chord(item.split("."))
            c.offset = offset
            output_stream.append(c)
        else:
            n = note.Note(item)
            n.offset = offset
            output_stream.append(n)

        offset += 0.5

    except Exception as e:
        print("Skipped invalid note:", item)
        continue

print("STEP 7: Writing MIDI file")

output_stream.write('midi', fp='generated_music.mid')

print("STEP 8: DONE - MIDI created")
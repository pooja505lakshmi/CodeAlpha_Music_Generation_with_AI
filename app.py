import streamlit as st
import os
from music21 import stream, note, chord
import numpy as np
import random
from tensorflow.keras.models import load_model

st.title("🎵 AI Music Generator")
st.write("Generate AI-created MIDI music using an LSTM model.")

model = load_model("music_model.keras")

with open("notes.txt", "r") as f:
    notes = [line.strip() for line in f]

pitchnames = sorted(set(notes))
note_to_int = {n: i for i, n in enumerate(pitchnames)}
int_to_note = {i: n for i, n in enumerate(pitchnames)}

if st.button("Generate Music"):

    sequence_length = 50

    start = random.randint(0, len(notes) - sequence_length)
    pattern = notes[start:start + sequence_length]

    output_notes = []

    for i in range(100):
        input_seq = [note_to_int[n] for n in pattern]
        input_seq = np.reshape(input_seq, (1, sequence_length, 1))
        input_seq = input_seq / float(len(pitchnames))

        prediction = model.predict(input_seq, verbose=0)
        index = np.argmax(prediction)

        result = int_to_note[index]

        output_notes.append(result)

        pattern.append(result)
        pattern = pattern[1:]

    offset = 0
    output_stream = stream.Stream()

    for item in output_notes:
        try:
            if item.isdigit():
                continue

            if "." in item:
                c = chord.Chord(item.split("."))
                c.offset = offset
                output_stream.append(c)
            else:
                n = note.Note(item)
                n.offset = offset
                output_stream.append(n)

            offset += 0.5

        except:
            pass

    output_stream.write("midi", fp="generated_music.mid")

    st.success("Music generated successfully!")

    with open("generated_music.mid", "rb") as file:
        st.download_button(
            label="⬇ Download MIDI File",
            data=file,
            file_name="generated_music.mid",
            mime="audio/midi"
        )
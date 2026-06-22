from music21 import converter, instrument, note, chord
import glob

notes = []

for midi_file in glob.glob("*/*.mid"):
    print("Reading:", midi_file)

    try:
        midi = converter.parse(midi_file)

        parts = instrument.partitionByInstrument(midi)

        if parts:
            notes_to_parse = parts.parts[0].recurse()
        else:
            notes_to_parse = midi.flatten().notes

        for element in notes_to_parse:
            if isinstance(element, note.Note):
                notes.append(str(element.pitch))
            elif isinstance(element, chord.Chord):
                notes.append('.'.join(str(n) for n in element.normalOrder))

    except Exception as e:
        print("Error:", midi_file, e)

print("\nTotal notes extracted:", len(notes))

with open("notes.txt", "w") as f:
    for n in notes:
        f.write(n + "\n")

print("Saved notes.txt")
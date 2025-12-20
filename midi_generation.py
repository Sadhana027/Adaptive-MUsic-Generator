import mido
from mido import MidiFile, MidiTrack, Message
from midi2audio import FluidSynth

def generate_midi(tempo, key, scale, instrument, chords, drums, output_file="output.mid", length=32):
    # Create a MIDI file and track
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    # Set tempo (microseconds per beat)
    microseconds_per_beat = int(60000000 / tempo)  # Convert BPM to microseconds per beat
    track.append(mido.MetaMessage('set_tempo', tempo=microseconds_per_beat))

    # Set instrument (program change)
    instrument_program = 0  # Default to Acoustic Grand Piano
    if instrument == "electric guitar":
        instrument_program = 27  # Electric Guitar (Clean)
    elif instrument == "acoustic guitar":
        instrument_program = 25  # Acoustic Guitar (Nylon)
    elif instrument == "strings":
        instrument_program = 49  # String Ensemble 1
    track.append(Message('program_change', program=instrument_program))

    # Ensure chords is a list of lists
    if isinstance(chords, int):
        chords = [[chords]]  # Wrap single integer in a list
    elif all(isinstance(chord, int) for chord in chords):
        chords = [chords]  # Wrap single chord in a list

    # Add chords
    for time in range(length):  # Iterate over the specified length
        chord = chords[time % len(chords)]  # Cycle through chords
        for note in chord:
            track.append(Message('note_on', note=note, velocity=64, time=0))
        for note in chord:
            track.append(Message('note_off', note=note, velocity=64, time=480))  # 480 ticks = 1 beat

    # Add drums (percussion track) on Channel 10
    drum_track = MidiTrack()
    mid.tracks.append(drum_track)
    for time in range(length):
        for drum_note in drums:
            # Add drum notes to Channel 10 (percussion channel)
            drum_track.append(Message('note_on', note=drum_note, velocity=64, time=0, channel=9))  # Channel 10 is index 9
            drum_track.append(Message('note_off', note=drum_note, velocity=64, time=240, channel=9))  # 240 ticks = half beat

    # Add melody (simple scale)
    if scale == "major":
        notes = [60, 62, 64, 65, 67, 69, 71, 72]  # C4 to C5 in the C major scale
    elif scale == "minor":
        notes = [57, 59, 60, 62, 64, 65, 67, 69]  # A3 to A4 in the A minor scale

    for time in range(length):
        note = notes[time % len(notes)]  # Cycle through notes
        track.append(Message('note_on', note=note, velocity=64, time=0))
        track.append(Message('note_off', note=note, velocity=64, time=240))  # 240 ticks = half beat

    # Save the MIDI file
    mid.save(output_file)
    print(f"MIDI file saved as {output_file}")

def convert_midi_to_wav(midi_file, soundfont, output_wav="output.wav"):
    fs = FluidSynth(soundfont)
    fs.midi_to_audio(midi_file, output_wav)
    print(f"MIDI converted to WAV: {output_wav}")

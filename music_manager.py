import heapq

import mido
import time
import tkinter as tk
from tkinter import filedialog
from mido import Message

class MIDIManager:
    def __init__(self):
        self.INSTRUMENTS = {
            0: "Acoustic Grand Piano",
            1: "Bright Acoustic Piano",
            2: "Electric Grand Piano",
            3: "Honky-tonk Piano",
            4: "Electric Piano 1",
            5: "Electric Piano 2",
            6: "Harpsichord",
            7: "Clavinet",
            8: "Celesta",
            9: "Glockenspiel",
            10: "Music Box",
            11: "Vibraphone",
            12: "Marimba",
            13: "Xylophone",
            14: "Tubular Bells",
            15: "Dulcimer",
            16: "Drawbar Organ",
            17: "Percussive Organ",
            18: "Rock Organ",
            19: "Church Organ",
            20: "Reed Organ",
            21: "Accordion",
            22: "Harmonica",
            23: "Tango Accordion",
            24: "Acoustic Guitar (nylon)",
            25: "Acoustic Guitar (steel)",
            26: "Electric Guitar (jazz)",
            27: "Electric Guitar (clean)",
            28: "Electric Guitar (muted)",
            29: "Overdriven Guitar",
            30: "Distortion Guitar",
            31: "Guitar Harmonics",
            32: "Acoustic Bass",
            33: "Electric Bass (finger)",
            34: "Electric Bass (pick)",
            35: "Fretless Bass",
            36: "Slap Bass 1",
            37: "Slap Bass 2",
            38: "Synth Bass 1",
            39: "Synth Bass 2",
            40: "Violin",
            41: "Viola",
            42: "Cello",
            43: "Contrabass",
            44: "Tremolo Strings",
            45: "Pizzicato Strings",
            46: "Orchestral Harp",
            47: "Timpani",
            48: "String Ensemble 1",
            49: "String Ensemble 2",
            50: "Synth Strings 1",
            51: "Synth Strings 2",
            52: "Choir Aahs",
            53: "Voice Oohs",
            54: "Synth Choir",
            55: "Orchestra Hit",
            56: "Trumpet",
            57: "Trombone",
            58: "Tuba",
            59: "Muted Trumpet",
            60: "French Horn",
            61: "Brass Section",
            62: "Synth Brass 1",
            63: "Synth Brass 2",
            64: "Soprano Sax",
            65: "Alto Sax",
            66: "Tenor Sax",
            67: "Baritone Sax",
            68: "Oboe",
            69: "English Horn",
            70: "Bassoon",
            71: "Clarinet",
            72: "Piccolo",
            73: "Flute",
            74: "Recorder",
            75: "Pan Flute",
            76: "Blown Bottle",
            77: "Shakuhachi",
            78: "Whistle",
            79: "Ocarina",
            80: "Lead 1 (square)",
            81: "Lead 2 (sawtooth)",
            82: "Lead 3 (calliope)",
            83: "Lead 4 (chiff)",
            84: "Lead 5 (charang)",
            85: "Lead 6 (voice)",
            86: "Lead 7 (fifths)",
            87: "Lead 8 (bass + lead)",
            88: "Pad 1 (new age)",
            89: "Pad 2 (warm)",
            90: "Pad 3 (polysynth)",
            91: "Pad 4 (choir)",
            92: "Pad 5 (bowed)",
            93: "Pad 6 (metallic)",
            94: "Pad 7 (halo)",
            95: "Pad 8 (sweep)",
            96: "FX 1 (rain)",
            97: "FX 2 (soundtrack)",
            98: "FX 3 (crystal)",
            99: "FX 4 (atmosphere)",
            100: "FX 5 (brightness)",
            101: "FX 6 (goblins)",
            102: "FX 7 (echoes)",
            103: "FX 8 (sci-fi)",
            104: "Sitar",
            105: "Banjo",
            106: "Shamisen",
            107: "Koto",
            108: "Kalimba",
            109: "Bagpipe",
            110: "Fiddle",
            111: "Shanai",
            112: "Tinkle Bell",
            113: "Agogo",
            114: "Steel Drums",
            115: "Woodblock",
            116: "Taiko Drum",
            117: "Melodic Tom",
            118: "Synth Drum",
            119: "Reverse Cymbal",
            120: "Guitar Fret Noise",
            121: "Breath Noise",
            122: "Seashore",
            123: "Bird Tweet",
            124: "Telephone Ring",
            125: "Helicopter",
            126: "Applause",
            127: "Gunshot"
        }
        self.INSTRUMENTS_REVERSED = {
            "Acoustic Grand Piano": 0,
            "Bright Acoustic Piano": 1,
            "Electric Grand Piano": 2,
            "Honky-tonk Piano": 3,
            "Electric Piano 1": 4,
            "Electric Piano 2": 5,
            "Harpsichord": 6,
            "Clavinet": 7,
            "Celesta": 8,
            "Glockenspiel": 9,
            "Music Box": 10,
            "Vibraphone": 11,
            "Marimba": 12,
            "Xylophone": 13,
            "Tubular Bells": 14,
            "Dulcimer": 15,
            "Drawbar Organ": 16,
            "Percussive Organ": 17,
            "Rock Organ": 18,
            "Church Organ": 19,
            "Reed Organ": 20,
            "Accordion": 21,
            "Harmonica": 22,
            "Tango Accordion": 23,
            "Acoustic Guitar (nylon)": 24,
            "Acoustic Guitar (steel)": 25,
            "Electric Guitar (jazz)": 26,
            "Electric Guitar (clean)": 27,
            "Electric Guitar (muted)": 28,
            "Overdriven Guitar": 29,
            "Distortion Guitar": 30,
            "Guitar Harmonics": 31,
            "Acoustic Bass": 32,
            "Electric Bass (finger)": 33,
            "Electric Bass (pick)": 34,
            "Fretless Bass": 35,
            "Slap Bass 1": 36,
            "Slap Bass 2": 37,
            "Synth Bass 1": 38,
            "Synth Bass 2": 39,
            "Violin": 40,
            "Viola": 41,
            "Cello": 42,
            "Contrabass": 43,
            "Tremolo Strings": 44,
            "Pizzicato Strings": 45,
            "Orchestral Harp": 46,
            "Timpani": 47,
            "String Ensemble 1": 48,
            "String Ensemble 2": 49,
            "Synth Strings 1": 50,
            "Synth Strings 2": 51,
            "Choir Aahs": 52,
            "Voice Oohs": 53,
            "Synth Choir": 54,
            "Orchestra Hit": 55,
            "Trumpet": 56,
            "Trombone": 57,
            "Tuba": 58,
            "Muted Trumpet": 59,
            "French Horn": 60,
            "Brass Section": 61,
            "Synth Brass 1": 62,
            "Synth Brass 2": 63,
            "Soprano Sax": 64,
            "Alto Sax": 65,
            "Tenor Sax": 66,
            "Baritone Sax": 67,
            "Oboe": 68,
            "English Horn": 69,
            "Bassoon": 70,
            "Clarinet": 71,
            "Piccolo": 72,
            "Flute": 73,
            "Recorder": 74,
            "Pan Flute": 75,
            "Blown Bottle": 76,
            "Shakuhachi": 77,
            "Whistle": 78,
            "Ocarina": 79,
            "Lead 1 (square)": 80,
            "Lead 2 (sawtooth)": 81,
            "Lead 3 (calliope)": 82,
            "Lead 4 (chiff)": 83,
            "Lead 5 (charang)": 84,
            "Lead 6 (voice)": 85,
            "Lead 7 (fifths)": 86,
            "Lead 8 (bass + lead)": 87,
            "Pad 1 (new age)": 88,
            "Pad 2 (warm)": 89,
            "Pad 3 (polysynth)": 90,
            "Pad 4 (choir)": 91,
            "Pad 5 (bowed)": 92,
            "Pad 6 (metallic)": 93,
            "Pad 7 (halo)": 94,
            "Pad 8 (sweep)": 95,
            "FX 1 (rain)": 96,
            "FX 2 (soundtrack)": 97,
            "FX 3 (crystal)": 98,
            "FX 4 (atmosphere)": 99,
            "FX 5 (brightness)": 100,
            "FX 6 (goblins)": 101,
            "FX 7 (echoes)": 102,
            "FX 8 (sci-fi)": 103,
            "Sitar": 104,
            "Banjo": 105,
            "Shamisen": 106,
            "Koto": 107,
            "Kalimba": 108,
            "Bagpipe": 109,
            "Fiddle": 110,
            "Shanai": 111,
            "Tinkle Bell": 112,
            "Agogo": 113,
            "Steel Drums": 114,
            "Woodblock": 115,
            "Taiko Drum": 116,
            "Melodic Tom": 117,
            "Synth Drum": 118,
            "Reverse Cymbal": 119,
            "Guitar Fret Noise": 120,
            "Breath Noise": 121,
            "Seashore": 122,
            "Bird Tweet": 123,
            "Telephone Ring": 124,
            "Helicopter": 125,
            "Applause": 126,
            "Gunshot": 127
        }

        self.ticks_per_beat = 480
        self.bpm = 120
    # def play_notes(self, notes, instrument):
    #     try:
    #         with mido.open_output() as midi_out:
    #             program_number = print(self.INSTRUMENTS_REVERSED[instrument])
    #             midi_out.send(mido.Message('program_change', program=program_number))
    #
    #             for (duration, start_time, volume, pitch) in notes:
    #                 midi_note = int(69 + 12 * math.log2(pitch / 440.0))
    #                 midi_note = max(0, min(127, midi_note))
    #
    #                 midi_velocity = max(0, min(127, int((volume + 100) / 2)))
    #
    #                 time.sleep(start_time / 1000)
    #                 midi_out.send(mido.Message('note_on', note=midi_note, velocity=midi_velocity))
    #
    #                 time.sleep(duration / 1000)
    #                 midi_out.send(mido.Message('note_off', note=midi_note))
    #     except Exception as e:
    #         print("Error", f"Failed to play notes: {e}")
    # def play_notes(self, notes, instrument):
    #     try:
    #         with mido.open_output() as midi_out:
    #             # Convert instrument index to program number
    #             program_number = instrument if isinstance(instrument, int) else self.INSTRUMENTS_REVERSED[instrument]
    #             midi_out.send(mido.Message('program_change', program=program_number))
    #
    #             for (duration, start_time, volume, pitch) in notes:
    #                 # Use pitch directly if it's a MIDI note number
    #                 midi_note = int(pitch)
    #
    #                 # Scale volume to MIDI velocity range
    #                 midi_velocity = max(0, min(127, int((volume + 100) / 2)))
    #
    #                 time.sleep(start_time / 1000)
    #                 midi_out.send(mido.Message('note_on', note=midi_note, velocity=midi_velocity))
    #
    #                 time.sleep(duration / 1000)
    #                 midi_out.send(mido.Message('note_off', note=midi_note))
    #     except Exception as e:
    #         print(f"Error: Failed to play notes: {e}")

    # def play_notes(self, notes, instrument):
    #     try:
    #         with mido.open_output() as midi_out:
    #             # Convert instrument index to program number
    #             program_number = instrument if isinstance(instrument, int) else self.INSTRUMENTS_REVERSED[instrument]
    #             midi_out.send(mido.Message('program_change', program=program_number))
    #
    #             # Sort notes by start_time to play them in order
    #             notes.sort(key=lambda n: n[1])  # Sort by start_time
    #
    #             start_time = time.time()  # Get the reference start time
    #
    #             active_notes = []  # Track active notes for stopping them later
    #
    #             for (duration, start_time_ms, volume, pitch) in notes:
    #                 # Calculate when this note should start
    #                 note_start_time = start_time + (start_time_ms / 1000.0)
    #
    #                 # Wait until it's time to play this note
    #                 while time.time() < note_start_time:
    #                     time.sleep(0.001)  # Sleep for a very short time to stay responsive
    #
    #                 # Convert pitch directly if it's a MIDI note number
    #                 midi_note = int(pitch)
    #                 midi_velocity = max(0, min(127, int((volume + 100) / 2)))  # Scale volume
    #
    #                 # Play the note
    #                 midi_out.send(mido.Message('note_on', note=midi_note, velocity=midi_velocity))
    #                 active_notes.append((midi_note, time.time() + (duration / 1000.0)))  # Store end time
    #
    #                 # Stop notes that should end
    #                 new_active_notes = []
    #                 for note, end_time in active_notes:
    #                     if time.time() >= end_time:
    #                         midi_out.send(mido.Message('note_off', note=note))
    #                     else:
    #                         new_active_notes.append((note, end_time))
    #                 active_notes = new_active_notes
    #
    #             # Ensure all remaining notes are stopped
    #             for note, _ in active_notes:
    #                 midi_out.send(mido.Message('note_off', note=note))
    #
    #     except Exception as e:
    #         print(f"Error: Failed to play notes: {e}")

    def play_notes(self, notes, instrument=0, midi_port = None):
        try:
            with mido.open_output() as output:
                output.send(Message('program_change', program=instrument))

                start_time = time.time()
                note_events = []

                # Create note events (on and off), converting ms to seconds
                for duration, start, volume, pitch in notes:
                    start_sec = start / 1000
                    duration_sec = duration / 1000
                    note_events.append((start_sec, 'note_on', pitch, volume))
                    note_events.append((start_sec + duration_sec, 'note_off', pitch, 0))

                # Sort events by time
                note_events.sort()

                for event_time, event_type, pitch, velocity in note_events:
                    while time.time() - start_time < event_time:
                        time.sleep(0.001)
                    output.send(Message(event_type, note=pitch, velocity=velocity))
        except Exception as e:
            print(f"Error: {e}")

    def export(self, notes, instrument=0, bpm=120):

        root = tk.Tk()
        root.withdraw()  # Hide main Tkinter window
        filename = filedialog.asksaveasfilename(
            defaultextension=".mid",
            filetypes=[("MIDI files", "*.mid")],
            title="Save MIDI File"
        )

        if not filename:
            print("Save canceled.")
            return

        mid = mido.MidiFile(ticks_per_beat=self.ticks_per_beat)
        track = mido.MidiTrack()
        mid.tracks.append(track)


        tempo = mido.bpm2tempo(self.bpm)
        track.append(mido.MetaMessage('set_tempo', tempo=tempo))

        track.append(mido.Message('program_change', program=instrument, time=0))

        ticks_per_second = (self.bpm / 60) * self.ticks_per_beat
        notes_sorted = sorted(notes, key=lambda n: n[1])

        last_time = 0

        for duration_ms, start_time_ms, volume, pitch in notes_sorted:
            start_tick = int(start_time_ms * (ticks_per_second / 1000))
            duration_tick = int(duration_ms * (ticks_per_second / 1000))

            delta_time = start_tick - last_time
            last_time = start_tick

            # Note On
            track.append(mido.Message('note_on', note=pitch + 21, velocity=volume, time=delta_time))
            # Note Off
            track.append(mido.Message('note_off', note=pitch + 21, velocity=0, time=duration_tick))

        # Save the MIDI file
        mid.save(filename)
        print(f"Exported to {filename} with instrument {instrument}")

# [(400, 0, -10, 440),(400, 400, -10, 494),(400, 800, -10, 523),(400, 1200, -10, 440)]

#[(400, 0, 64, 69), (400, 400, 64, 71), (400, 800, 64, 72), (400, 1200, 64, 69)]
#
# testthing =  MIDIManager()
# testthing.play_notes([(400, 0, 64, 69), (400, 400, 64, 71), (400, 800, 64, 72), (400, 1200, 64, 69)], 0)



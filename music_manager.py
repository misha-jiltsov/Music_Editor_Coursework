import mido
import time
import tkinter as tk
from tkinter import filedialog
from mido import Message
import pymsgbox


class MIDIManager:
    def __init__(self):

        self.INSTRUMENTS = {}
        self.INSTRUMENTS_REVERSED = {}

        with open("INSTRUMENTS.txt", "r") as f:
            for i, line in enumerate(f.readlines()):
                self.INSTRUMENTS[i] = line.strip("\n")
                self.INSTRUMENTS_REVERSED[line.strip("\n")] = i

        self.ticks_per_beat = 480 # default values for exporting and playing
        self.bpm = 120 # default values for exporting and playing


    def play_notes(self, notes, instrument=0):
        try:
            with mido.open_output() as output:
                output.send(Message('program_change', program=instrument))  # change the instrument to the selected instrument

                start_time = time.time()
                note_events = []

                # Create note events, converting milliseconds to seconds
                for duration, start, volume, pitch in notes:
                    start_secnd = start / 1000
                    dur_sec = duration / 1000
                    note_events.append((start_secnd, 'note_on', pitch, volume))
                    note_events.append((start_secnd + dur_sec, 'note_off', pitch, 0))

                # Sort events by time
                note_events.sort()

                for event_time, event_type, pitch, velocity in note_events: # plays every note using the note events
                    while time.time() - start_time < event_time:
                        time.sleep(0.001)
                    output.send(Message(event_type, note=pitch, velocity=velocity))
        except Exception as e:
            pymsgbox.alert(f"Error {e}", "Error") # return an error if anything fails

    def export(self, notes, instrument=0, bpm=120):

        root = tk.Tk()
        root.withdraw()  # Hide main Tkinter window
        filename = filedialog.asksaveasfilename(
            defaultextension=".mid",
            filetypes=[("MIDI files", "*.mid")], # defaults for file window, ensured proper export
            title="Save MIDI File"
        )

        if not filename:
            pymsgbox.alert("Save Cancelled", "Error")  # error popup if no file selected
            return

        mid = mido.MidiFile(ticks_per_beat=self.ticks_per_beat) # create file
        track = mido.MidiTrack() # create current track
        mid.tracks.append(track) # add track to file


        tempo = mido.bpm2tempo(self.bpm) # set the tempo for the export file
        track.append(mido.MetaMessage('set_tempo', tempo=tempo))

        track.append(mido.Message('program_change', program=instrument, time=0))

        ticks_per_second = (self.bpm / 60) * self.ticks_per_beat
        notes_sorted = sorted(notes, key=lambda n: n[1])

        last_time = 0

        for duration_ms, start_time_ms, volume, pitch in notes_sorted: # loop through sorted notes and add them to the file
            start_tick = int(start_time_ms * (ticks_per_second / 1000))
            duration_tick = int(duration_ms * (ticks_per_second / 1000))

            delta_time = start_tick - last_time
            last_time = start_tick

            track.append(mido.Message('note_on', note=pitch + 21, velocity=volume, time=delta_time))
            track.append(mido.Message('note_off', note=pitch + 21, velocity=0, time=duration_tick))

        mid.save(filename)
        pymsgbox.alert(f"Exported to {filename} with instrument {instrument}", "Info") # tell the user the data has been exported using a popup


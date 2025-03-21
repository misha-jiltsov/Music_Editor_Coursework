import wx
from grid2 import PianoRollPanel
from music_manager import MIDIManager
import json
import tkinter as tk
from tkinter import filedialog
from database_manager import Database_Manager

class DAWFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.SetTitle("DAW")
        self.SetSize((1500, 920))
        self.instruments = []
        with open("INSTRUMENTS.txt", "r") as f:
            for line in f.readlines():
                self.instruments.append(line.strip())

        self.Music_Player = MIDIManager()
        self.database_manager = Database_Manager()

        self.shift_start_time = False

        panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        left_panel = wx.Panel(panel, size=(200, -1))
        left_sizer = wx.BoxSizer(wx.VERTICAL)

        self.item_list = wx.ListBox(left_panel, choices=self.instruments, style=wx.LB_SINGLE)
        left_sizer.Add(self.item_list, 1, wx.EXPAND | wx.ALL, 5)

        self.recent_files_list = wx.ListCtrl(left_panel, style=wx.LC_REPORT)
        self.recent_files_list.InsertColumn(0, 'Filename', width=200)
        self.recent_files_list.InsertColumn(1, 'Date Created', width=150)

        left_sizer.Add(self.recent_files_list)

        left_panel.SetSizer(left_sizer)

        main_sizer.Add(left_panel, 0, wx.EXPAND | wx.ALL, 5)

        # Right panel: Controls and Piano Roll Grid
        right_panel = wx.Panel(panel)
        right_sizer = wx.BoxSizer(wx.VERTICAL)

        # Controls section
        controls_box = wx.StaticBox(right_panel, label="Controls")
        controls_panel = wx.StaticBoxSizer(controls_box, wx.HORIZONTAL)
        play_button = wx.Button(right_panel, label="Play")
        get_data_button = wx.Button(right_panel, label="Get all data")
        clear_board_button = wx.Button(right_panel, label="Clear Track")
        export_button = wx.Button(right_panel, label="Export Track")
        save_track_button = wx.Button(right_panel, label="Save Track")
        load_track_button = wx.Button(right_panel, label="Load Existing Track")
        self.checkbox = wx.CheckBox(right_panel, label="Shift Note Start time")
        self.checkbox.Bind(wx.EVT_CHECKBOX, self.on_time_checkbox_toggle)
        self.remove_note_toggle = wx.CheckBox(right_panel, label="Remove Note")
        self.remove_note_toggle.Bind(wx.EVT_CHECKBOX, self.on_remove_checkbox_toggle)

        controls_panel.Add(play_button, 0, wx.ALL, 5)
        controls_panel.Add(get_data_button, 0, wx.ALL, 5)
        controls_panel.Add(clear_board_button, 0, wx.ALL, 5)
        controls_panel.Add(export_button, 0, wx.ALL, 5)
        controls_panel.Add(save_track_button, 0, wx.ALL, 5)
        controls_panel.Add(load_track_button, 0, wx.ALL, 5)
        controls_panel.Add(self.checkbox, 0, wx.ALL, 8)
        controls_panel.Add(self.remove_note_toggle, 0, wx.ALL, 8)



        play_button.Bind(wx.EVT_BUTTON, self.play_current_track)
        get_data_button.Bind(wx.EVT_BUTTON, self.show_all_notes_terminal)
        clear_board_button.Bind(wx.EVT_BUTTON, self.clear_track)
        export_button.Bind(wx.EVT_BUTTON, self.export_track)
        save_track_button.Bind(wx.EVT_BUTTON, self.save_track_to_file)
        load_track_button.Bind(wx.EVT_BUTTON, self.load_saved_track)
        right_sizer.Add(controls_panel, 0, wx.EXPAND | wx.ALL, 5)

        # Piano Roll Grid section
        piano_roll_box = wx.StaticBox(right_panel, label="Piano Roll")
        piano_roll_sizer = wx.StaticBoxSizer(piano_roll_box, wx.VERTICAL)
        self.piano_roll_panel = PianoRollPanel(right_panel, num_notes=35, num_beats=64)
        piano_roll_sizer.Add(self.piano_roll_panel, 1, wx.EXPAND | wx.ALL, 5)
        right_sizer.Add(piano_roll_sizer, 1, wx.EXPAND | wx.ALL, 5)

        # Note Input section
        note_input_box = wx.StaticBox(right_panel, label="Note Input")
        note_input_panel = wx.StaticBoxSizer(note_input_box, wx.HORIZONTAL)
        self.duration_input = wx.TextCtrl(right_panel, size=(50, -1))
        self.duration_input.SetValue("1")  # duration in beats
        self.time_input = wx.TextCtrl(right_panel, size=(50, -1))
        self.time_input.SetValue("0")
        self.volume_input = wx.TextCtrl(right_panel, size=(50, -1))
        self.volume_input.SetValue("100")
        self.pitch_input = wx.TextCtrl(right_panel, size=(50, -1))
        self.pitch_input.SetValue("60")
        add_note_button = wx.Button(right_panel, label="Add Note")
        add_note_button.Bind(wx.EVT_BUTTON, self.on_add_note)

        note_input_panel.Add(wx.StaticText(right_panel, label="Duration:"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        note_input_panel.Add(self.duration_input, 0, wx.ALL, 5)
        note_input_panel.Add(wx.StaticText(right_panel, label="Start Time:"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        note_input_panel.Add(self.time_input, 0, wx.ALL, 5)
        note_input_panel.Add(wx.StaticText(right_panel, label="Volume:"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        note_input_panel.Add(self.volume_input, 0, wx.ALL, 5)
        note_input_panel.Add(wx.StaticText(right_panel, label="Pitch:"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        note_input_panel.Add(self.pitch_input, 0, wx.ALL, 5)
        note_input_panel.Add(add_note_button, 0, wx.ALL, 5)

        right_sizer.Add(note_input_panel, 0, wx.EXPAND | wx.ALL, 5)

        right_panel.SetSizer(right_sizer)
        main_sizer.Add(right_panel, 1, wx.EXPAND | wx.ALL, 5)
        panel.SetSizer(main_sizer)

        self.playable_notes = []

    def export_track(self, event):
        self.refresh_clean_notes()
        instrument = self.item_list.GetStringSelection()
        self.Music_Player.export(self.playable_notes, self.instruments.index(instrument))

    def on_time_checkbox_toggle(self, event):
        self.shift_start_time = self.checkbox.IsChecked()

    def on_remove_checkbox_toggle(self, event):
        self.piano_roll_panel.delete_note = self.remove_note_toggle.IsChecked()

    def clear_track(self, event):
        self.piano_roll_panel.notes = []
        self.piano_roll_panel.Refresh()

    def on_print_selected_item(self, event):
        selected_item = self.item_list.GetStringSelection()
        if selected_item:
            print(f"Selected Item: {selected_item}")
        else:
            print("No item selected.")

    def play_current_track(self, event):
        instrument = self.item_list.GetStringSelection()
        self.refresh_clean_notes()
        print(self.playable_notes)
        if instrument:
            print(self.piano_roll_panel.notes, self.instruments.index(instrument))
            self.Music_Player.play_notes(self.playable_notes, self.instruments.index(instrument))
        else:
            print("No instrument selected.")

    def show_all_notes_terminal(self, event):
        print("All notes in Piano Roll:")
        for note in self.piano_roll_panel.notes:
            print(note)
        print(self.playable_notes)

    def refresh_clean_notes(self):
        self.playable_notes = []
        for note in self.piano_roll_panel.notes:
            duration = 400*(note[1]-note[0])
            start_time = 400*(note[0])
            volume = int(self.volume_input.GetValue())
            pitch = note[2]
            self.playable_notes.append((duration, start_time, volume, pitch+39))
        print("playable notes" , self.playable_notes)

    def on_add_note(self, event):
        try:
            start_beat = int(self.time_input.GetValue())
            duration = int(self.duration_input.GetValue())
            pitch = int(self.pitch_input.GetValue())
        except ValueError:
            print("Invalid input")
            return
        end_beat = start_beat + duration
        self.piano_roll_panel.notes.append((start_beat, end_beat, pitch))
        self.piano_roll_panel.Refresh()
        if self.shift_start_time:
            new_start = start_beat + duration
            self.time_input.SetValue(str(new_start))

    def save_track_to_file(self, event):
        note_dict = {}
        self.refresh_clean_notes()

        for note_id, note in enumerate(self.piano_roll_panel.notes):
            start_beat, end_beat, pitch = note
            note_dict[note_id] = {"start_beat": start_beat,
                                  "end_beat": end_beat,
                                  "pitch": pitch}

        file_selection = tk.Tk()
        file_selection.withdraw()  # hides the main tkinter windows
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json")],
            title="Save Track Layout"
        )

        if not filename:
            print("Save canceled.")
            return

        with open(filename, "w") as save_file:
            json.dump(note_dict, save_file, indent=4)



    def load_saved_track(self, event):

        file_selection = tk.Tk()
        file_selection.withdraw()
        filename = filedialog.askopenfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json")],
            title="Open Saved Track"
        )


        if not filename:
            print("Save canceled.")
            return


        with open(filename, "r") as loaded_file:
            loaded_data = json.load(loaded_file)

        self.piano_roll_panel.notes = []

        for i in range(len(loaded_data)):
            self.piano_roll_panel.notes.append(tuple([int(x) for x in loaded_data[str(i)].values()]))

        self.refresh_clean_notes()
        self.piano_roll_panel.Refresh()

    def update_recent_files(self):
        recent_files = self.database_manager.get_recent_tracks(10)

        self.recent_files_list.DeleteAllItems()

        for idx, (filename, date_created) in enumerate(recent_files):
            self.recent_files_list.InsertItem(idx, filename)
            self.recent_files_list.SetItem(idx, 1, date_created)

    def update_database(self, filename, filepath):

        self.database_manager.update_data()




if __name__ == "__main__":
    app = wx.App(False)
    frame = DAWFrame(None)
    frame.Show()
    app.MainLoop()

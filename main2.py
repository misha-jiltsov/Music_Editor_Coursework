import wx
from grid2 import PianoRollPanel
from music_manager import MIDIManager
import json
import tkinter as tk
from tkinter import filedialog
from database_manager import Database_Manager
import pymsgbox

class DAWFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Setting up the GUI
        self.SetTitle("DAW")
        self.SetSize((1650, 920))

        #retrieves instruments from saved text file
        self.instruments = []
        with open("INSTRUMENTS.txt", "r") as f:
            for line in f.readlines():
                self.instruments.append(line.strip())

        self.Music_Player = MIDIManager() # created MIDIManager Object, responsible for note playing
        self.database_manager = Database_Manager() # responsible for managing storing data

        self.shift_start_time = False # decides if timing on manual input is incremented
        self.recent_filepath = None # track selected on recent files list

        panel = wx.Panel(self)  # main panel, contains all the widgets in the program
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        left_panel = wx.Panel(panel, size=(350, -1)) # stores the instrument list and the recent tracks
        left_sizer = wx.BoxSizer(wx.VERTICAL)

        #### all left components

        self.item_list = wx.ListBox(left_panel, choices=self.instruments, style=wx.LB_SINGLE)
        left_sizer.Add(self.item_list, 1, wx.EXPAND | wx.ALL, 5)

        self.recent_files_list = wx.ListCtrl(left_panel, style=wx.LC_REPORT)
        self.recent_files_list.InsertColumn(0, 'Filename', width=200)
        self.recent_files_list.InsertColumn(1, 'Date Created', width=150)
        self.recent_files_list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_item_selected)

        self.database_manager.check_files_exists_remove_missing() # remove any deleted files on startup
        self.update_recent_files() # refresh the recent files

        load_from_recent_button = wx.Button(left_panel, label="Load File") # creates button to load from recent

        left_sizer.Add(self.recent_files_list)
        left_sizer.Add(load_from_recent_button, 0, wx.EXPAND | wx.ALL, 5)

        load_from_recent_button.Bind(wx.EVT_BUTTON, self.on_load_button) # binds the button, every time it is clicked
                                                                         # the method will run
        left_panel.SetSizer(left_sizer)

        main_sizer.Add(left_panel, 0, wx.EXPAND | wx.ALL, 5)

        # Right panel:Controls and Piano Roll
        right_panel = wx.Panel(panel)
        right_sizer = wx.BoxSizer(wx.VERTICAL)

        # All the controls
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


        # Adding all the controls to the control panel
        controls_panel.Add(play_button, 0, wx.ALL, 5)
        controls_panel.Add(get_data_button, 0, wx.ALL, 5)
        controls_panel.Add(clear_board_button, 0, wx.ALL, 5)
        controls_panel.Add(export_button, 0, wx.ALL, 5)
        controls_panel.Add(save_track_button, 0, wx.ALL, 5)
        controls_panel.Add(load_track_button, 0, wx.ALL, 5)
        controls_panel.Add(self.checkbox, 0, wx.ALL, 8)

        # Binds each of buttons to their corresponding methods
        play_button.Bind(wx.EVT_BUTTON, self.play_current_track)
        get_data_button.Bind(wx.EVT_BUTTON, self.show_all_notes_terminal)
        clear_board_button.Bind(wx.EVT_BUTTON, self.clear_track)
        export_button.Bind(wx.EVT_BUTTON, self.export_track)
        save_track_button.Bind(wx.EVT_BUTTON, self.save_track_to_file)
        load_track_button.Bind(wx.EVT_BUTTON, self.load_saved_track)

        right_sizer.Add(controls_panel, 0, wx.EXPAND | wx.ALL, 5) # addes the control panel to the right section
        # as it is added first, it is on top of the right sizer

        # Piano Roll section
        piano_roll_box = wx.StaticBox(right_panel, label="Piano Roll")
        piano_roll_sizer = wx.StaticBoxSizer(piano_roll_box, wx.VERTICAL)
        self.piano_roll_panel = PianoRollPanel(right_panel, num_notes=35, num_beats=64)
        piano_roll_sizer.Add(self.piano_roll_panel, 1, wx.EXPAND | wx.ALL, 5)
        right_sizer.Add(piano_roll_sizer, 1, wx.EXPAND | wx.ALL, 5)

        # Manual Note input section
        note_input_box = wx.StaticBox(right_panel, label="Note Input")
        note_input_panel = wx.StaticBoxSizer(note_input_box, wx.HORIZONTAL)
        self.duration_input = wx.TextCtrl(right_panel, size=(50, -1))
        self.duration_input.SetValue("1")  # set default duration in beats to 1
        self.time_input = wx.TextCtrl(right_panel, size=(50, -1))
        self.time_input.SetValue("0") # set default time value
        self.volume_input = wx.TextCtrl(right_panel, size=(50, -1))
        self.volume_input.SetValue("100") # set default volume value
        self.pitch_input = wx.TextCtrl(right_panel, size=(50, -1))
        self.pitch_input.SetValue("60")  # set default pitch value
        add_note_button = wx.Button(right_panel, label="Add Note")
        add_note_button.Bind(wx.EVT_BUTTON, self.on_add_note)

        ## Adding all fo the inputs to the input panel
        note_input_panel.Add(wx.StaticText(right_panel, label="Duration:"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        note_input_panel.Add(self.duration_input, 0, wx.ALL, 5)
        note_input_panel.Add(wx.StaticText(right_panel, label="Start Time:"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        note_input_panel.Add(self.time_input, 0, wx.ALL, 5)
        note_input_panel.Add(wx.StaticText(right_panel, label="Volume:"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        note_input_panel.Add(self.volume_input, 0, wx.ALL, 5)
        note_input_panel.Add(wx.StaticText(right_panel, label="Pitch:"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        note_input_panel.Add(self.pitch_input, 0, wx.ALL, 5)
        note_input_panel.Add(add_note_button, 0, wx.ALL, 5)

        right_sizer.Add(note_input_panel, 0, wx.EXPAND | wx.ALL, 5) # add the note panel to the right sizer

        right_panel.SetSizer(right_sizer)
        main_sizer.Add(right_panel, 1, wx.EXPAND | wx.ALL, 5) # add the right panel to the main sizer
        panel.SetSizer(main_sizer)

        self.playable_notes = [] # clear the playable notes list



    def export_track(self, event):
        self.refresh_clean_notes()                                                        # updates notes in proper format
        instrument = self.item_list.GetStringSelection()                                  # gets selected instrument
        self.Music_Player.export(self.playable_notes, self.instruments.index(instrument)) # exports track to a file using

    def on_time_checkbox_toggle(self, event):
        self.shift_start_time = self.checkbox.IsChecked() # toggles start time variable on and off with button press

    def clear_track(self, event):
        self.piano_roll_panel.notes = [] # removes all existing notes
        self.piano_roll_panel.Refresh() # refreshes piano roll, showing the new blank state

    def on_load_button(self, event):
        if self.recent_filepath is not None:
            try:
                self.load_saved_track(event, filepath=self.recent_filepath[0][0]) # try to load user saved file
            except:
                pymsgbox.alert(f"Error Loading Recent File", "Error") # return error if failed
                # potential reasons for fail:
                # - invalid file format
                # - invalid file type
                # - variables out of range

    def on_item_selected(self, event): # bound to recent files list box
        selected_index = self.recent_files_list.GetFirstSelected() # retrieves selected item index (could be -1 if nothing selected)

        if selected_index != -1:  # Check if an item is selected
            filename = self.recent_files_list.GetItemText(selected_index, 0)
            self.recent_filepath = self.database_manager.get_path_from_name(filename) # gets filepath from selected filename
        event.Skip()

    def play_current_track(self, event):
        instrument = self.item_list.GetStringSelection() # check selected instrument
        self.refresh_clean_notes() # update the correctly formatted notes
        if instrument: # check if instrument selected
            self.Music_Player.play_notes(self.playable_notes, self.instruments.index(instrument)) # use local music player to play the notes
        else:
            pymsgbox.alert("No Instrument Selected", "Error")

    def show_all_notes_terminal(self, event): # shows all notes in the terminal, mainly for debugging
        print("All notes in Piano Roll:")
        for note in self.piano_roll_panel.notes:
            print(note)
        print(self.playable_notes)

    def refresh_clean_notes(self):                          # formatting the notes to fit the export properly
        self.playable_notes = []                            # clear current notes
        for note in self.piano_roll_panel.notes:            # loop through existing notes
            duration = 400*(note[1]-note[0])                # convert duration from beats to milliseconds
            start_time = 400*(note[0])                      # convert to milliseconds
            volume = int(self.volume_input.GetValue())      # converts to an integer
            pitch = note[2]
            self.playable_notes.append((duration, start_time, volume, pitch+39)) # adds note as a tuple

    def on_add_note(self, event):                                          # method binds manual note adding button
        try:
            start_beat = int(self.time_input.GetValue())
            duration = int(self.duration_input.GetValue())
            pitch = int(self.pitch_input.GetValue())
        except ValueError:                                                 # raises error if a value is an incorrect type or missing
            pymsgbox.alert("Invalid Input", "Error")
            return
        end_beat = start_beat + duration
        self.piano_roll_panel.notes.append((start_beat, end_beat, pitch))  # adds note to piano roll
        self.piano_roll_panel.Refresh()                                    # refreshes piano roll to display note
        if self.shift_start_time:                                          # shifts start time if selected
            new_start = start_beat + duration
            self.time_input.SetValue(str(new_start))

    def save_track_to_file(self, event):
        note_dict = {}  # create blank dictionary to export
        self.refresh_clean_notes()

        for note_id, note in enumerate(self.piano_roll_panel.notes):  # converts all the data to a dictionary form
            start_beat, end_beat, pitch = note
            note_dict[note_id] = {"start_beat": start_beat,
                                  "end_beat": end_beat,
                                  "pitch": pitch}

        file_selection = tk.Tk()
        file_selection.withdraw()  # hides the main tkinter windows
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json")],  # defaults for the file explorer window,
            title="Save Track Layout"              # makes sure user file selection is correct
        )

        if not file_path: # does not continue if user does not select file, prevents errors
            pymsgbox.alert("Canceled Save", "Error")
            return

        with open(file_path, "w") as save_file:
            json.dump(note_dict, save_file, indent=4)  # exports the dictionary of notes into a file

        filename = file_path.split("/")[-1] # gets filename from file path

        self.update_database(filename, file_path)
        self.update_recent_files()

    def load_saved_track(self, event, filepath=None):

        if filepath == None:
            file_selection = tk.Tk()
            file_selection.withdraw()
            filepath = filedialog.askopenfilename(
                defaultextension=".json",
                filetypes=[("JSON Files", "*.json")], # defaults for the file explorer window,
                title="Open Saved Track"              # makes sure user file selection is correct
            )

            if not filepath:
                pymsgbox.alert("Canceled Loading File", "Error") # returns error if file not selected
                return

        with open(filepath, "r") as loaded_file:
            loaded_data = json.load(loaded_file) # read the selected json file

        self.piano_roll_panel.notes = [] # remove all notes, essentially clearing the current track

        for i in range(len(loaded_data)):
            self.piano_roll_panel.notes.append(tuple([int(x) for x in loaded_data[str(i)].values()])) # load up all the new data

        self.refresh_clean_notes()      # refreshes local notes
        self.piano_roll_panel.Refresh() # refresh display

    def update_recent_files(self):
        recent_files = self.database_manager.get_recent_tracks(5)
        self.database_manager.check_files_exists_remove_missing()
        self.recent_files_list.DeleteAllItems()

        for id, (filename, date_created) in enumerate(recent_files):
            self.recent_files_list.InsertItem(id, filename)
            self.recent_files_list.SetItem(id, 1, date_created)

    def update_database(self, filename, filepath):
        self.database_manager.update_data(filename, filepath)


if __name__ == "__main__":
    app = wx.App(False)
    frame = DAWFrame(None)
    frame.Show()
    app.MainLoop()

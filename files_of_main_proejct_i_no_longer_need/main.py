
#TODO
# make the track tab
# add instruments on the left
# improve track display
# make music play in real time
# fix following bugs:
#   - notes not being removes from self.notes when removed in the gui
#   - same issue as above but with tracks
#   - music broken (not playing in real time anymore)
# connect music and GUI together
# make exports work to mp4 and/or MIDI




import wx
import wx.lib.scrolledpanel as scrolled
from music_manager import MIDIManager




class DAWFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.SetTitle("DAW")
        self.SetSize((1000, 600))
        self.notes = []
        self.instruments = []
        with open("../INSTRUMENTS.txt", "r") as f:
            for line in f.readlines():
                self.instruments.append(line.strip())

        self.Music_Player = MIDIManager()

        self.shift_start_time = False


        panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        left_panel = wx.Panel(panel, size=(200, -1))
        left_sizer = wx.BoxSizer(wx.VERTICAL)

        self.item_list = wx.ListBox(left_panel, choices=self.instruments, style=wx.LB_SINGLE)
        left_sizer.Add(self.item_list, 1, wx.EXPAND | wx.ALL, 5)

        print_button = wx.Button(left_panel, label="Print Selected Item")
        print_button.Bind(wx.EVT_BUTTON, self.on_print_selected_item)
        left_sizer.Add(print_button, 0, wx.EXPAND | wx.ALL, 5)

        left_panel.SetSizer(left_sizer)
        main_sizer.Add(left_panel, 0, wx.EXPAND | wx.ALL, 5)

        right_panel = wx.Panel(panel)
        right_sizer = wx.BoxSizer(wx.VERTICAL)

        controls_box = wx.StaticBox(right_panel, label="Controls")
        controls_panel = wx.StaticBoxSizer(controls_box, wx.HORIZONTAL)

        play_button = wx.Button(right_panel, label="Play")
        pause_button = wx.Button(right_panel, label="Pause")
        stop_button = wx.Button(right_panel, label="Stop")
        get_data_button = wx.Button(right_panel, label="Get all data")
        self.checkbox = wx.CheckBox(right_panel, label="Shift Note Start time")
        self.checkbox.Bind(wx.EVT_CHECKBOX, self.on_checkbox_toggle)

        controls_panel.Add(play_button, 0, wx.ALL, 5)
        controls_panel.Add(pause_button, 0, wx.ALL, 5)
        controls_panel.Add(stop_button, 0, wx.ALL, 5)
        controls_panel.Add(get_data_button, 0, wx.ALL, 5)
        controls_panel.Add(self.checkbox, 0, wx.ALL, 8)

        get_data_button.Bind(wx.EVT_BUTTON, self.show_all_notes_terminal)
        play_button.Bind(wx.EVT_BUTTON, self.play_current_track)


        right_sizer.Add(controls_panel, 0, wx.EXPAND | wx.ALL, 5)

        tracks_box = wx.StaticBox(right_panel, label="Tracks")
        tracks_sizer = wx.StaticBoxSizer(tracks_box, wx.VERTICAL)

        self.scroll_panel = scrolled.ScrolledPanel(right_panel, size=(-1, 300),
                                                   style=wx.TAB_TRAVERSAL | wx.BORDER_SUNKEN)
        self.scroll_panel.SetAutoLayout(1)
        self.scroll_panel.SetupScrolling(scroll_x=False, scroll_y=True)

        self.tracks_panel = wx.BoxSizer(wx.VERTICAL)
        self.scroll_panel.SetSizer(self.tracks_panel)

        tracks_sizer.Add(self.scroll_panel, 1, wx.EXPAND | wx.ALL, 5)
        right_sizer.Add(tracks_sizer, 1, wx.EXPAND | wx.ALL, 5)

        track_buttons_panel = wx.Panel(right_panel)
        track_buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)

        add_track_button = wx.Button(track_buttons_panel, label="Add Track")
        remove_track_button = wx.Button(track_buttons_panel, label="Remove Track")

        add_track_button.Bind(wx.EVT_BUTTON, self.on_add_track)
        remove_track_button.Bind(wx.EVT_BUTTON, self.on_remove_track)

        track_buttons_sizer.Add(add_track_button, 0, wx.ALL, 5)
        track_buttons_sizer.Add(remove_track_button, 0, wx.ALL, 5)

        track_buttons_panel.SetSizer(track_buttons_sizer)
        right_sizer.Add(track_buttons_panel, 0, wx.EXPAND | wx.ALL, 5)

        note_input_box = wx.StaticBox(right_panel, label="Note Input")
        note_input_panel = wx.StaticBoxSizer(note_input_box, wx.HORIZONTAL)

        self.track_selector = wx.ComboBox(right_panel, choices=[], style=wx.CB_READONLY)
        self.track_selector.Bind(wx.EVT_COMBOBOX, self.on_track_selected)
        self.duration_input = wx.TextCtrl(right_panel, size=(50, -1))
        self.duration_input.SetValue("400")
        self.time_input = wx.TextCtrl(right_panel, size=(50, -1))
        self.time_input.SetValue("0")
        self.volume_input = wx.TextCtrl(right_panel, size=(50, -1))
        self.volume_input.SetValue("100")
        self.pitch_input = wx.TextCtrl(right_panel, size=(50, -1))
        self.pitch_input.SetValue("69")
        add_note_button = wx.Button(right_panel, label="Add Note")

        add_note_button.Bind(wx.EVT_BUTTON, self.on_add_note)

        note_input_panel.Add(wx.StaticText(right_panel, label="Select Track:"), 0,
                             wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        note_input_panel.Add(self.track_selector, 0, wx.ALL, 5)
        note_input_panel.Add(wx.StaticText(right_panel, label="Duration:"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        note_input_panel.Add(self.duration_input, 0, wx.ALL, 5)
        note_input_panel.Add(wx.StaticText(right_panel, label="Start Time:"), 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                             5)
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

        self.track_count = 0
        self.track_panels = []

    def on_checkbox_toggle(self, event):
        if self.checkbox.IsChecked():
            self.shift_start_time = True
        else:
            self.shift_start_time = False

    def on_print_selected_item(self, event):
        selected_item = self.item_list.GetStringSelection()
        if selected_item:
            print(f"Selected Item: {selected_item}")
        else:
            print("No item selected.")

    def get_all_notes(self):
        return self.notes

    def play_current_track(self, event):
        current_track, current_instrument = self.get_track_data()
        print(self.notes[current_track-1][1:], self.instruments.index(current_instrument))
        self.Music_Player.play_notes(self.notes[current_track-1][1:], self.instruments.index(current_instrument))

    def get_track_data(self):
        current_track = str(self.track_selector.GetValue())
        print(current_track)
        track_index = int(current_track.split("\t")[0].split(" ")[1])
        track_instrument = current_track.split("\t")[1][1:-1]
        print(track_index, track_instrument)
        return track_index, track_instrument

    def on_add_track(self, event):
        if self.item_list.GetStringSelection()!=None:
            track_box = wx.StaticBox(self.scroll_panel, label=f"Track {self.track_count+1}\t({self.item_list.GetStringSelection()})")
            track_panel = wx.StaticBoxSizer(track_box, wx.VERTICAL)

            note_sizer = wx.BoxSizer(wx.VERTICAL)
            track_panel.Add(note_sizer, 1, wx.EXPAND | wx.ALL, 5)

            self.tracks_panel.Add(track_panel, 0, wx.EXPAND | wx.ALL, 5)
            self.track_panels.append((track_panel, note_sizer))
            self.track_selector.Append(f"Track {self.track_count+1}\t({self.item_list.GetStringSelection()})")

            if self.track_count > 0:
                track_panel.GetStaticBox().Hide()

            self.scroll_panel.Layout()
            self.scroll_panel.FitInside()
            self.scroll_panel.SetupScrolling(scroll_x=False, scroll_y=True)

            self.track_count += 1

            self.show_selected_track()

            #####################################################

            self.notes.append([self.item_list.GetStringSelection()])

    def on_remove_track(self, event):
        selected_track = self.track_selector.GetSelection()
        if selected_track != wx.NOT_FOUND:
            track_panel, _ = self.track_panels.pop(selected_track)
            self.tracks_panel.Hide(track_panel)
            self.tracks_panel.Remove(track_panel)
            self.track_selector.Delete(selected_track)
            self.notes.pop(selected_track)

            self.track_count -= 1
            self.scroll_panel.Layout()
            self.scroll_panel.FitInside()


    def show_all_notes_terminal(self, event):
        for tracknum, track in enumerate(self.notes):
            print(f"Track {tracknum}:")
            for note in track[1:]:
                print(note)

    def on_add_note(self, event):
        selected_track = self.track_selector.GetSelection()
        if selected_track != wx.NOT_FOUND:
            _, note_sizer = self.track_panels[selected_track]

            duration = self.duration_input.GetValue()
            start_time = self.time_input.GetValue()
            volume = self.volume_input.GetValue()
            pitch = self.pitch_input.GetValue()

            self.notes[int(selected_track)].append((int(duration), int(start_time), int(volume), int(pitch)))

            note_panel = wx.Panel(self.scroll_panel)
            note_label = wx.StaticText(note_panel, label=f"Duration: {duration}, Start: {start_time}, Volume: {volume}, Pitch: {pitch}")
            # remove_note_button = GUI_note(len(self.notes[int(selected_track)]), note_panel, label="Remove Note")
            # remove_note_button.Bind(wx.EVT_BUTTON, self.on_remove_note)

            remove_note_button = wx.Button(note_panel, label="Remove Note")
            remove_note_button.Bind(wx.EVT_BUTTON, self.on_remove_note)

            note_panel_sizer = wx.BoxSizer(wx.HORIZONTAL)
            note_panel_sizer.Add(note_label, 1, wx.ALIGN_CENTER_VERTICAL)
            note_panel_sizer.Add(remove_note_button, 0, wx.ALL, 5)
            note_panel.SetSizer(note_panel_sizer)

            note_sizer.Add(note_panel, 0, wx.EXPAND | wx.ALL, 5)

            self.scroll_panel.Layout()
            self.scroll_panel.FitInside()

            if self.shift_start_time:
                temp_thing = int(self.time_input.GetValue())
                self.time_input.Clear()
                self.time_input.write(str(int(self.duration_input.GetValue())+temp_thing))


    def on_remove_note(self, event):
        # button = event.GetEventObject()
        # note_panel = button.GetParent()
        # note_sizer = note_panel.GetContainingSizer()
        #
        # note_index = button.get_location_in_track()
        # track_index, _ = self.get_track_data()
        #
        # self.notes[track_index-1].pop(note_index)
        #
        # if note_sizer:
        #     note_sizer.Detach(note_panel)
        #     note_panel.Destroy()
        #
        #
        #
        # self.scroll_panel.Layout()
        # self.scroll_panel.FitInside()


        # Which button was clicked?
        button = event.GetEventObject()
        # The parent panel that holds the label + Remove button
        note_panel = button.GetParent()

        # Which track is currently selected (e.g. "Track 1")?
        track_index, _ = self.get_track_data()  # this returns e.g. (1, "InstrumentName")

        # Get the sizer that holds all the note_panels for this track
        note_sizer = note_panel.GetContainingSizer()
        if not note_sizer:
            return  # safety check, should never happen if your layout is correct

        # Find the index of note_panel in the sizer's children
        children = note_sizer.GetChildren()
        note_index = None
        for i, child in enumerate(children):
            # child.GetWindow() is a wx.Window (our note_panel)
            if child.GetWindow() == note_panel:
                note_index = i
                break

        if note_index is None:
            return  # didn't find the panel for some reason

        # Because self.notes[track_index - 1][0] is the instrument name,
        # the actual first note is at index 1. So we pop note_index + 1.
        self.notes[track_index - 1].pop(note_index + 1)

        # Remove the panel from the sizer and destroy it
        note_sizer.Detach(note_panel)
        note_panel.Destroy()

        # Re-layout
        self.scroll_panel.Layout()
        self.scroll_panel.FitInside()

    def show_selected_track(self):
        selected_track = self.track_selector.GetSelection()

        for i, (track_panel, note_sizer) in enumerate(self.track_panels):
            for note_panel in note_sizer.GetChildren():
                note_panel.GetWindow().Hide()

        _, selected_note_sizer = self.track_panels[selected_track]
        for note_panel in selected_note_sizer.GetChildren():
            note_panel.GetWindow().Show()

        for i, (track_panel, _) in enumerate(self.track_panels):
            if i == selected_track:
                track_panel.GetStaticBox().Show()
            else:
                track_panel.GetStaticBox().Hide()

        self.scroll_panel.Layout()
        self.scroll_panel.FitInside()

    def on_track_selected(self, event):
        self.show_selected_track()


# class GUI_note(wx.Button):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args[1:], **kwargs)
#         self.index = args[0]
#
#     def get_location_in_track(self):
#         return self.index
#
#     def set_location_in_track(self, index):
#         self.index = index

class GridRoll(wx.GridSizer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)




if __name__ == "__main__":
    app = wx.App(False)
    frame = DAWFrame(None)
    frame.Show()
    app.MainLoop()


import wx
import music_manager, grid2
class DAWApp(wx.Frame):
    def __init__(self):
        super().__init__(None, title="DAW", size=(1500, 920))

        self.SetBackgroundColour(wx.Colour(20, 20, 20))  # Dark background
        panel = wx.Panel(self)
        panel.SetBackgroundColour(wx.Colour(30, 30, 30))
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.instruments = []
        with open("INSTRUMENTS.txt", "r") as f:
            for line in f.readlines():
                self.instruments.append(line.strip())

        self.Music_Player = music_manager.MIDIManager()
        self.shift_start_time = False

        left_panel = wx.Panel(panel, size=(200, -1))
        left_panel.SetBackgroundColour(wx.Colour(40, 40, 40))
        left_sizer = wx.BoxSizer(wx.VERTICAL)

        self.item_list = wx.ListBox(left_panel, choices=self.instruments, style=wx.LB_SINGLE)
        self.item_list.SetBackgroundColour(wx.Colour(50, 50, 50))
        self.item_list.SetForegroundColour(wx.Colour(200, 200, 200))
        left_sizer.Add(self.item_list, 1, wx.EXPAND | wx.ALL, 5)

        print_button = wx.Button(left_panel, label="Print Selected Item")
        print_button.SetBackgroundColour(wx.Colour(60, 60, 60))
        print_button.SetForegroundColour(wx.Colour(200, 200, 200))

        left_sizer.Add(print_button, 0, wx.EXPAND | wx.ALL, 5)

        left_panel.SetSizer(left_sizer)
        main_sizer.Add(left_panel, 0, wx.EXPAND | wx.ALL, 5)

        right_panel = wx.Panel(panel)
        right_panel.SetBackgroundColour(wx.Colour(30, 30, 30))
        right_sizer = wx.BoxSizer(wx.VERTICAL)

        controls_sizer = wx.BoxSizer(wx.HORIZONTAL)

        play_button = wx.Button(right_panel, label="▶ Play")
        play_button.SetBackgroundColour(wx.Colour(60, 60, 60))
        play_button.SetForegroundColour(wx.Colour(200, 200, 200))

        controls_sizer.Add(play_button, 0, wx.ALL, 5)

        stop_button = wx.Button(right_panel, label="■ Stop")
        stop_button.SetBackgroundColour(wx.Colour(60, 60, 60))
        stop_button.SetForegroundColour(wx.Colour(200, 200, 200))
        controls_sizer.Add(stop_button, 0, wx.ALL, 5)

        get_data_button = wx.Button(right_panel, label="Get all data")
        get_data_button.SetBackgroundColour(wx.Colour(60, 60, 60))
        get_data_button.SetForegroundColour(wx.Colour(200, 200, 200))

        controls_sizer.Add(get_data_button, 0, wx.ALL, 5)

        clear_board_button = wx.Button(right_panel, label="Clear Track")
        clear_board_button.SetBackgroundColour(wx.Colour(60, 60, 60))
        clear_board_button.SetForegroundColour(wx.Colour(200, 200, 200))

        controls_sizer.Add(clear_board_button, 0, wx.ALL, 5)

        right_sizer.Add(controls_sizer, 0, wx.EXPAND | wx.ALL, 5)

        self.piano_roll_panel = wx.Panel(right_panel, size=(900, 500))
        self.piano_roll_panel.SetBackgroundColour(wx.Colour(20, 20, 20))
        right_sizer.Add(self.piano_roll_panel, 1, wx.EXPAND | wx.ALL, 5)

        right_panel.SetSizer(right_sizer)
        main_sizer.Add(right_panel, 1, wx.EXPAND | wx.ALL, 5)

        panel.SetSizer(main_sizer)
        self.Show()

if __name__ == "__main__":
    app = wx.App(False)
    frame = DAWApp()
    app.MainLoop()

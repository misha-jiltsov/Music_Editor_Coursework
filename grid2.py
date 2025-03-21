import wx

class PianoRollPanel(wx.Panel):
    def __init__(self, parent, num_notes, num_beats):
        super(PianoRollPanel, self).__init__(parent)
        self.SetBackgroundColour(wx.Colour(50, 50, 50))
        self.beat_width = 80
        self.note_height = 20
        self.num_beats = num_beats
        self.num_notes = num_notes
        self.delete_note = False

        # Set a minimum size for the panel based on beats and notes
        self.SetMinSize((self.beat_width * self.num_beats + 40, self.note_height * self.num_notes))

        self.notes = []  # Each note is stored as a tuple: (start_beat, end_beat, pitch)
        self.dragging = False
        self.current_note = None
        self.SetDoubleBuffered(True)

        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_LEFT_DOWN, self.on_left_down)
        self.Bind(wx.EVT_LEFT_UP, self.on_left_up)
        self.Bind(wx.EVT_MOTION, self.on_motion)
        self.Bind(wx.EVT_SIZE, self.on_resize)


    def on_paint(self, event):
        dc = wx.PaintDC(self)
        self.draw_piano_roll(dc)

    def draw_piano_roll(self, dc):
        dc.SetBrush(wx.Brush(wx.Colour(255, 255, 255)))
        for note in range(self.num_notes):
            y = note * self.note_height
            pitch = self.num_notes - (y // self.note_height) - 1
            dc.DrawRectangle(0, y, 40, self.note_height)
            # dc.DrawText(self.get_Note_Name_from_pitch(pitch), 0, y)
            dc.DrawText(str(self.get_Note_Name_from_pitch(pitch+39)), 0, y)

        dc.SetPen(wx.Pen(wx.Colour(100, 100, 100), 1))
        for beat in range(self.num_beats + 1):
            x = 40 + beat * self.beat_width
            dc.DrawLine(x, 0, x, self.num_notes * self.note_height)

        # Draw horizontal grid lines (notes)
        for note in range(self.num_notes + 1):
            y = note * self.note_height
            dc.DrawLine(40, y, 40 + self.num_beats * self.beat_width, y)

        # Draw the notes as green rectangles
        dc.SetBrush(wx.Brush(wx.Colour(0, 255, 0)))
        for note in self.notes:
            start_beat, end_beat, pitch = note
            x = 40 + start_beat * self.beat_width
            y = (self.num_notes - pitch - 1) * self.note_height
            width = (end_beat - start_beat) * self.beat_width
            dc.DrawRectangle(x, y, width, self.note_height)

    def get_Note_Name_from_pitch(self, i):
        note_dict = {0: "C", 1: "D", 2: "E", 3: "F", 4: "G", 5: "A", 6: "B"}
        return (str(note_dict[(i + 3) % 7]) + str((i - 4) // 7 - 4))

    def on_left_down(self, event):
        pos = event.GetPosition()
        # Check if clicking on an existing note to drag it
        if self.delete_note == False:
            for i, note in enumerate(self.notes):
                start_beat, end_beat, pitch = note
                x = 40 + start_beat * self.beat_width
                y = (self.num_notes - pitch - 1) * self.note_height
                width = (end_beat - start_beat) * self.beat_width
                if x <= pos.x <= x + width and y <= pos.y <= y + self.note_height:
                    self.dragging = True
                    self.current_note = i
                    break
            else:
                # Otherwise, add a new note at the clicked location
                beat = (pos.x - 40) // self.beat_width
                pitch = self.num_notes - (pos.y // self.note_height) - 1
                if pos.x>40:
                    self.notes.append((beat, beat + 1, pitch))
                    self.current_note = len(self.notes) - 1
                    self.dragging = True
        else:
            beat = (pos.x - 40) // self.beat_width
            pitch = self.num_notes - (pos.y // self.note_height) - 1
            if (beat, beat+1, pitch) in self.notes:
                self.notes.remove((beat, beat+1, pitch))
        self.Refresh()

    def on_left_up(self, event):
        self.dragging = False
        self.current_note = None

    def on_motion(self, event):
        if self.dragging and self.current_note is not None:
            pos = event.GetPosition()
            if pos.x > 40 and pos.y < self.note_height * self.num_notes:
                beat = (pos.x - 40) // self.beat_width
                pitch = self.num_notes - (pos.y // self.note_height) - 1
                start_beat, end_beat, _ = self.notes[self.current_note]
                duration = end_beat - start_beat
                self.notes[self.current_note] = (beat, beat + duration, pitch)
                self.Refresh()

    def on_resize(self, event):
        self.Refresh()

if __name__ == "__main__":
    app = wx.App(False)
    frame = wx.Frame(None, title="Piano Roll")
    panel = PianoRollPanel(frame, num_notes=50, num_beats=64)
    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.Add(panel, 1, wx.EXPAND)
    frame.SetSizer(sizer)
    frame.Show()
    app.MainLoop()

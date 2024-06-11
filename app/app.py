import wx
import wx.media
import logging


class VideoPlayerFrame(wx.Frame):
    """
    The parent for everything in the wx user interface.
    """

    def __init__(self, title):
        super(VideoPlayerFrame, self).__init__(parent=None, title=title, size=(1280, 720),
                                               style=wx.RESIZE_BORDER | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN | wx.FRAME_NO_TASKBAR)

        logging.debug("Initializing video player frame")
        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Video player.
        self.video_player = VideoPlayer(panel)
        sizer.Add(self.video_player, 2, wx.EXPAND | wx.ALL, border=0)

        # Text panel.
        self.text_panel = TextPanel(panel)
        sizer.Add(self.text_panel, 1, wx.EXPAND | wx.ALL, border=0)

        panel.SetSizer(sizer)

        # Events.
        self.Bind(wx.EVT_CHAR_HOOK, self.on_key_press)

    def on_key_press(self, event):
        """
        This function is called when a key is pressed.
        Its primary purpose is to check for keyboard shortcuts being pressed.
        """
        if event.ControlDown():
            keycode = event.GetKeyCode()
            if keycode == ord('P'):  # Play/Pause
                # todo pause
                self.video_player.play_video()
            elif keycode == ord('O'):  # Open file dialog
                # todo put into its own function
                logging.debug("Open file dialog key pressed")
                open_dialog = wx.FileDialog(self, "Open", "", "", "Video files (*.mp4)|*.mp4",
                                            wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
                if open_dialog.ShowModal() == wx.ID_CANCEL:
                    return
                file_path = open_dialog.GetPath()
                self.video_player.media.Load(file_path)
                open_dialog.Destroy()
        event.Skip()


class VideoPlayer(wx.Panel):
    def __init__(self, parent):
        super(VideoPlayer, self).__init__(parent)
        logging.debug("Initializing video player")

        self.SetBackgroundColour(wx.BLACK)

        # The video panel will parent both the video and placeholder.
        #self.video_panel = wx.Panel(self)

        self.media = wx.media.MediaCtrl(self, style=wx.SIMPLE_BORDER)

        # Create the placeholder.
        # todo potentially create placeholder logo

        # Create timeline.
        # todo create custom timeline class with ability to highlight segments with code
        self.timeline = HighlightTimeline(self)

        # Create a timer to update the timeline
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update_timeline, self.timer)
        self.timer.Start(100)  # Update every 100 milliseconds (0.1 second)

        # Layout.
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.media, 2, wx.EXPAND)
        sizer.Add(self.timeline, 0, wx.EXPAND | wx.ALL, border=5)
        self.SetSizer(sizer)

    def play_video(self):
        if self.media.GetState() == wx.media.MEDIASTATE_PLAYING:
            self.media.Pause()
            logging.debug("Video playing is now paused")
        else:
            self.media.Play()
            logging.debug("Video playing is now playing")

    def update_timeline(self, event):
        # Update the slider position to match the current video play time
        if self.media.Length() > 0:
            current_time = self.media.Tell() / 1000  # Convert milliseconds to seconds
            total_time = self.media.Length() / 1000  # Total duration in seconds
            if total_time > 0:
                self.timeline.set_thumb_position(current_time / total_time)


class HighlightTimeline(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.TAB_TRAVERSAL)
        self.highlights = []  # Highlight ranges
        self.thumb_position = 0.0  # Float position (0.0 to 1.0)
        self.Bind(wx.EVT_PAINT, self.on_paint)

        logging.debug("Initializing highlight timeline")
    def add_highlight_range(self, start: float, end: float):
        self.highlights.append((start, end))
        self.Refresh()

    def set_thumb_position(self, value):
        self.thumb_position = value
        self.Refresh()

    def on_paint(self, event):
        dc = wx.BufferedPaintDC(self)
        gc = wx.GraphicsContext.Create(dc)
        width, height = self.GetClientSize()

        # Draw the background of the timeline.
        gc.SetPen(wx.Pen(wx.BLACK, 1))
        gc.SetBrush(wx.Brush(wx.WHITE))
        gc.DrawRectangle(0, height // 2 - 5, width, 10)

        # Draw the highlighted ranges.
        for start, end in self.highlights:
            gc.SetPen(wx.Pen(wx.BLUE, 1))
            gc.SetBrush(wx.Brush(wx.BLUE))
            start_pos = width * start
            end_pos = width * end
            gc.DrawRectangle(start_pos, height // 2 - 5, end_pos - start_pos, 10)

        # Draw the thumb at the new position.
        thumb_pos = width * self.thumb_position
        gc.SetPen(wx.Pen(wx.BLACK, 1))
        gc.SetBrush(wx.Brush(wx.GREEN))
        gc.DrawRectangle(thumb_pos - 5, height // 2 - 5, 10, 10)


class TextPanel(wx.Panel):
    def __init__(self, parent):
        super(TextPanel, self).__init__(parent)
        self.text_ctrl = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_NO_VSCROLL)

        logging.debug("Initializing text panel")
        # Layout.
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.text_ctrl, 1, wx.EXPAND | wx.ALL, border=0)
        self.SetSizer(sizer)

    def update_text(self, text):
        self.text_ctrl.SetValue(text)


if __name__ == '__main__':
    app = wx.App()
    video_player = VideoPlayerFrame(title='OcrRoo')
    video_player.Show(True)
    app.MainLoop()
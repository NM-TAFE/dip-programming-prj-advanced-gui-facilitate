import wx
import wx.media


class VideoPlayerFrame(wx.Frame):
    """
    The parent for everything in the wx user interface.
    """

    def __init__(self, title):
        super(VideoPlayerFrame, self).__init__(parent=None, title=title, size=(1280, 720),
                                               style=wx.RESIZE_BORDER | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN | wx.FRAME_NO_TASKBAR)

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

        self.SetBackgroundColour(wx.BLACK)

        # The video panel will parent both the video and placeholder.
        #self.video_panel = wx.Panel(self)

        self.media = wx.media.MediaCtrl(self, style=wx.SIMPLE_BORDER)

        # Create the placeholder.
        # todo potentially create placeholder logo

        # Create timeline.
        # todo create custom timeline class with ability to highlight segments with code
        self.timeline = wx.Slider(self)

        # Layout.
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.media, 2, wx.EXPAND)
        sizer.Add(self.timeline, 0, wx.EXPAND | wx.ALL, border=2)
        self.SetSizer(sizer)


    def play_video(self):
        if self.media.GetState() == wx.media.MEDIASTATE_PLAYING:
            self.media.Pause()
        else:
            self.media.Play()


class TextPanel(wx.Panel):
    def __init__(self, parent):
        super(TextPanel, self).__init__(parent)
        self.text_ctrl = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_NO_VSCROLL)

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

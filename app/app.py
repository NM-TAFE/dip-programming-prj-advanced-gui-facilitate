import wx
import wx.media
import logging
from typing import Callable


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

        # Create menu bar listings.
        menu_bar = MenuBar()
        menu_bar.create_media_menu(self.video_player.open_file, self.on_quit)
        menu_bar.create_help_menu(self.on_shortcut_dialog)
        self.SetMenuBar(menu_bar)

        # Events.
        self.Bind(wx.EVT_CHAR_HOOK, self.on_key_press)

    def on_key_press(self, event):
        """
        This function is called when a key is pressed.
        Its primary purpose is to check for keyboard shortcuts being pressed.
        """
        keycode = event.GetKeyCode()
        if event.ControlDown():  # Ctrl
            if keycode == ord('O'):  # Ctrl+O - Open file dialog
                self.video_player.open_file()
            elif keycode == ord('Q'):  # Ctrl+Q - Quit
                self.on_quit(event)
        elif keycode == wx.WXK_SPACE:  # Space - Play/Pause
            self.video_player.play_video()
        elif keycode == wx.WXK_LEFT:  # ← - Skip back
            self.video_player.skip_timeline(-2)
        elif keycode == wx.WXK_RIGHT:  # → - Skip forward
            self.video_player.skip_timeline(2)
        elif keycode == wx.WXK_UP:  # ↑ - Volume up
            self.video_player.update_volume(0.1)
        elif keycode == wx.WXK_DOWN:  # ↓ - Volume down
            self.video_player.update_volume(-0.1)
        event.Skip()

    def on_quit(self, event=None):
        self.Close()

    def on_shortcut_dialog(self, event=None):
        about_dialog = ShortcutDialog(self)
        about_dialog.ShowModal()


class MenuBar(wx.MenuBar):
    def __init__(self):
        super(MenuBar, self).__init__()

    def create_media_menu(self, open_func: Callable, quit_func: Callable):
        media_menu = wx.Menu()
        open_file_item = media_menu.Append(wx.ID_ANY, 'Open File\tCtrl-O')
        self.Bind(wx.EVT_MENU, open_func, open_file_item)

        quit_item = media_menu.Append(wx.ID_ANY, 'Quit\tCtrl-P')
        self.Bind(wx.EVT_MENU, quit_func, quit_item)

        self.Append(media_menu, "Media")

    def create_help_menu(self, shortcut_dialog_func: Callable):
        help_menu = wx.Menu()
        shortcut_item = help_menu.Append(wx.ID_ANY, 'Keyboard Shortcuts')
        self.Bind(wx.EVT_MENU, shortcut_dialog_func, shortcut_item)

        self.Append(help_menu, "Help")


class ShortcutDialog(wx.Dialog):
    def __init__(self, parent):
        super(ShortcutDialog, self).__init__(parent, title="About")

        sizer = wx.BoxSizer(wx.VERTICAL)

        shortcuts = [
            "Ctrl+O: Open File",
            "Ctrl+Q: Quit",
            "Space: Play/Pause",
            "Left/Right Arrows: Skip Forward/Back",
            "Up/Down Arrows: Volume Up/Down",
        ]

        for shortcut in shortcuts:
            text = wx.StaticText(self, label=shortcut)
            sizer.Add(text, 0, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(sizer)
        self.Layout()


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

    """
    Shortcut functions
    """

    def open_file(self, event=None):
        logging.debug("Open file dialog key pressed")
        open_dialog = wx.FileDialog(self, "Open", "", "", "Video files (*.mp4)|*.mp4",
                                    wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if open_dialog.ShowModal() == wx.ID_CANCEL:
            return
        file_path = open_dialog.GetPath()
        self.media.Load(file_path)
        open_dialog.Destroy()

    def play_video(self):
        if self.media.GetState() == wx.media.MEDIASTATE_PLAYING:
            self.media.Pause()
            logging.debug("Video playing is now paused")
        else:
            self.media.Play()
            logging.debug("Video playing is now playing")

    def update_volume(self, increment: float):
        new_volume = self.media.GetVolume() + increment
        clamped_volume = max(0.0, min(new_volume, 1.0))  # Clamp volume between 0.0 and 1.0
        self.media.SetVolume(clamped_volume)

    def skip_timeline(self, seconds: int):
        current_position = self.media.Tell()
        new_position = current_position + seconds * 1000
        self.media.Seek(new_position)

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

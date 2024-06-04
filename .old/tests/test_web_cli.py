from app import web_cli
from tests.test_utils import load_dummy_user_data


def test_parse_command_cls():
    assert web_cli.parse_command("cls") == "clear"


def test_parse_command_clear():
    assert web_cli.parse_command("clear") == "clear"


def test_parse_command_help(mocker):
    mocker.patch("app.utils.read_from_file", return_value="dummy help menu")
    assert web_cli.parse_command("help") == "dummy help menu"


def test_parse_command_capture():
    assert web_cli.parse_command("capture") == "capture"


def test_parse_command_open():
    assert web_cli.parse_command("open") == "open"


def test_parse_command_list_videos(mocker):
    mocker.patch("app.web_cli.list_videos", return_value="dummy video list")
    assert web_cli.parse_command("list-videos") == "dummy video list"


def test_parse_command_available_videos(mocker):
    mocker.patch("app.web_cli.available_videos", return_value="dummy video list")
    assert web_cli.parse_command("available-videos") == "dummy video list"


def test_parse_command_play_video_invalid_command():
    assert web_cli.parse_command("play-video") == "<span class=\"text-red-500\">Invalid usage of play-video. Video " \
                                                  "must be specified. Type help for more information</span>"


def test_parse_command_navigate_home():
    assert web_cli.parse_command("navigate home") == {"redirect_page": "/"}


def test_parse_command_navigate_upload():
    assert web_cli.parse_command("navigate upload") == {"redirect_page": "/upload"}


def test_parse_command_navigate_collaborate():
    assert web_cli.parse_command("navigate collaborate") == {"redirect_page": "/collaborate"}


def test_parse_command_navigate_settings():
    assert web_cli.parse_command("navigate settings") == {"redirect_page": "/settings"}


def test_parse_command_play_video_valid(mocker):
    mocker.patch("app.utils.filename_exists_in_userdata", return_value=True)
    assert web_cli.parse_command("play-video my_video.mp4") == {"play_video": "my_video.mp4"}


def test_parse_command_play_video_invalid_video(mocker):
    mocker.patch("app.utils.filename_exists_in_userdata", return_value=False)
    assert web_cli.parse_command("play-video bad_video.mp4") == "<span class=\"text-red-500\">Failed to open video " \
                                                                "\"bad_video.mp4\", file does not exist</span>"


def test_parse_command_invalid_command():
    assert web_cli.parse_command("format") == "<span class=\"text-red-500\">Invalid command \"format\", type help " \
                                              "for more information</span>"


def test_available_videos(mocker):
    mocker.patch("app.utils.read_user_data", return_value=load_dummy_user_data())
    available_videos = web_cli.available_videos()
    assert available_videos[0] == "oop.mp4"
    assert available_videos[1] == "loops.mp4"
    assert available_videos[2] == "list_ops_handwriting.mp4"


def test_available_videos_none(mocker):
    mocker.patch("app.utils.read_user_data", return_value=None)
    assert web_cli.available_videos() == {}


def test_list_videos(mocker):
    mocker.patch("app.utils.read_user_data", return_value=load_dummy_user_data())
    list_videos = web_cli.list_videos()
    assert "oop.mp4" in list_videos
    assert "loops.mp4" in list_videos
    assert "list_ops_handwriting.mp4" in list_videos


def test_list_videos_empty(mocker):
    mocker.patch("app.utils.read_user_data", return_value=None)
    assert web_cli.list_videos() == "<p class='text-red-500'>No videos found in your library.<p>"

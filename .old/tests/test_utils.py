"""
This module contains the unit tests for the utility functions defined in app/utils.py.

Usage:
Run these tests using the pytest framework from the root of the project directory:
    $ pytest

Note: These tests use the pytest-mock plugin to replace calls to external resources with mock objects, ensuring that
tests remain fast and do not modify external state.
"""
import os

from app import utils


def load_dummy_user_data():
    """
    Dummy data for testing various functions in utils.py
    :return: Simulated user data in a dict
    """
    return {"all_videos": [{"video_hash": "b6a0f3d4d9d7f7f33fd53148e9a48d48", "filename": "oop.mp4",
                            "alias": "oop.mp4", "thumbnail": "1699007823.png", "video_length": 632, "progress": 341,
                            "captures": []},
                           {"video_hash": "8e3fed7fc8b8620469ea36703a5dfa94", "filename": "loops.mp4",
                            "alias": "loops.mp4",
                            "thumbnail": "1699007837.png", "video_length": 418, "progress": 0, "captures": []},
                           {"video_hash": "a0c0194cb4c5531a030fe68c8db304f9", "filename": "list_ops_handwriting.mp4",
                            "alias": "list_ops_handwriting.mp4", "thumbnail": "1699007846.png", "video_length": 186,
                            "progress": 186, "captures": [{"timestamp": 8, "capture_content": "dummy capture"}]}]}


def test_file_exists_in_user_data_true(mocker):
    mocker.patch("app.utils.read_user_data", return_value=load_dummy_user_data())
    assert utils.filename_exists_in_userdata("loops.mp4")


def test_file_exists_in_user_data_false(mocker):
    mocker.patch("app.utils.read_user_data", return_value=load_dummy_user_data())
    assert not utils.filename_exists_in_userdata("does_not_exist.mp4")


def test_file_exists_in_user_data_empty_user_data(mocker):
    mocker.patch("app.utils.read_user_data", return_value=None)
    assert not utils.filename_exists_in_userdata("hello-world.mp4")


def test_parse_video_data(mocker):
    mocker.patch("app.utils.read_user_data", return_value=load_dummy_user_data())
    parsed_video_data = utils.parse_video_data()
    assert len(parsed_video_data["all_videos"]) == 3
    assert len(parsed_video_data["continue_watching"]) == 2
    assert parsed_video_data["continue_watching"][0]["filename"] == "oop.mp4"
    assert parsed_video_data["continue_watching"][1]["filename"] == "loops.mp4"
    assert parsed_video_data["all_videos"][0]["filename"] == "oop.mp4"
    assert parsed_video_data["all_videos"][1]["filename"] == "loops.mp4"
    assert parsed_video_data["all_videos"][2]["filename"] == "list_ops_handwriting.mp4"


def test_parse_video_data_empty_user_data(mocker):
    mocker.patch("app.utils.read_user_data", return_value=None)
    parsed_video_data = utils.parse_video_data()
    assert parsed_video_data["all_videos"] is None
    assert parsed_video_data["continue_watching"] is None


def test_delete_video_from_user_data(mocker):
    mocker.patch("app.utils.read_user_data", return_value=load_dummy_user_data())
    mocker.patch("app.utils.open")
    utils.delete_video_from_userdata("loops.mp4")
    assert not utils.filename_exists_in_userdata("loops.mp4")


def test_delete_video_from_user_data_video_not_exist(mocker):
    mocker.patch("app.utils.read_user_data", return_value=load_dummy_user_data())
    mocker.patch("app.utils.open")
    utils.delete_video_from_userdata("ocr_training_video.mp4")
    assert not utils.filename_exists_in_userdata("ocr_training_video.mp4")


def test_delete_video_from_user_data_no_user_data(mocker):
    mocker.patch("app.utils.read_user_data", return_value=None)
    utils.delete_video_from_userdata("hello_world.mp4")
    assert not utils.filename_exists_in_userdata("hello_world.mp4")


def test_format_youtube_video_name():
    test_video_name_data = {
        "  This is    a   really long       bad video  name .mp4   ": "This_is_a_really_long_bad_video_name.mp4",
        "Python   tutorial  (unit testing   and   mocking).mp4": "Python_tutorial_(unit_testing_and_mocking).mp4",
        "hello world in ruby on rails": "hello_world_in_ruby_on_rails",
        "           ": "",
        "": "",
        None: None
    }
    for data in test_video_name_data:
        assert utils.format_youtube_video_name(data) == test_video_name_data[data]


def test_get_file_extension_for_current_language(mocker):
    programming_languages = {
        'python': '.py', 'javascript': '.js', 'java': '.java', 'c': '.c', 'c++': '.h',
        "fake_language": ".txt", "": ".txt"
    }
    for language in programming_languages:
        mocker.patch("app.utils.config", return_value=language)
        assert utils.get_file_extension_for_current_language() == programming_languages[language]


def test_hash_string():
    test_strings = {
        "hello world!": "fc3ff98e8c6a0d3087d515c0473f8677",
        "goodbye planet": "2f2149576f25995d4b2a5b7a00ff6f7e",
        "this is a string": "b37e16c620c055cf8207b999e3270e9b"
    }
    for string in test_strings:
        assert utils.hash_string(string) == test_strings[string]


def test_get_output_path(mocker):
    test_output_paths = {
        "c:\\users\\program files\\app": "c:\\users\\program files\\app\\",
        "output_path": os.path.dirname(os.getcwd()) + "\\out\\",
        "videos\\my_videos\\": "videos\\my_videos\\",
    }
    for paths in test_output_paths:
        mocker.patch("app.utils.config", return_value=paths)
        assert utils.get_output_path() == test_output_paths[paths]


def test_file_already_exists_true(mocker):
    mocker.patch("app.utils.read_user_data", return_value=load_dummy_user_data())
    assert utils.file_already_exists("8e3fed7fc8b8620469ea36703a5dfa94")


def test_file_already_exists_false(mocker):
    mocker.patch("app.utils.read_user_data", return_value=load_dummy_user_data())
    assert not utils.file_already_exists("8ak5sa6sk4d5akj56dh7kdh9ad6648")


def test_file_already_exists_no_user_data(mocker):
    mocker.patch("app.utils.read_user_data", return_value=None)
    assert not utils.file_already_exists("4aj3sdl5a4k2sjd091u091j")

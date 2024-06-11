import os.path
import logging
import shutil
from typing import Optional
import utils
import web_cli
from extract_text import ExtractText
from flask import Flask, render_template, request, send_file, redirect
import html
import glob

# Initialise flask app
app = Flask(__name__, static_url_path='/static', static_folder='static')
# Current video
filename: Optional[str] = None
# Flag to check if the search process should be canceled
cancel_search_flag: bool = False


@app.context_processor
def utility_processor():
    """
    Utility processor to send all hotkeys from config file to views/templates
    :return: Object containing all hotkeys
    """
    return {
        "hotkeys": utils.config()["Hotkeys"]
    }


@app.route("/")
def index():
    """
    Return the home page view/template with setup progress and parsed video data
    :return: Rendered template for home page
    """
    parsed_video_data = utils.parse_video_data()
    return render_template("index.html",
                           continue_watching=parsed_video_data["continue_watching"],
                           all_videos=parsed_video_data["all_videos"], setup_progress=utils.get_setup_progress())


@app.route("/settings")
def settings():
    """
    Return the settings view/template
    :return: Rendered template for settings page
    """
    current_settings = utils.get_current_settings()
    return render_template("settings.html", current_settings=current_settings)


@app.route("/web_cli", methods=['POST'])
def web_cli_endpoint():
    """
    Ajax endpoint for web cli commands
    :return: Response from web_cli parser as string or dict
    """
    data = request.get_json()
    return web_cli.parse_command(data["command"])


@app.route("/collaborate")
def collaborate():
    """
    Return collaborate start view/template
    :return: Rendered template for collaborate start page
    """
    return render_template("collaborate.html")


@app.route("/collaborate/create")
def create_collaborate():
    """
    Return collaborate create view/template
    :return: Rendered template for collaborate create page
    """
    return render_template("collaborate-create.html")


@app.route("/collaborate/join")
def join_collaborate():
    """
    Return collaborate join view/template
    :return: Rendered template for join collaborate page
    """
    pass


@app.route("/upload")
def upload():
    """
    Return upload video view/template with YouTube config variable
    :return: Rendered template for upload page
    """
    return render_template("upload.html",
                           use_youtube_downloader=eval(utils.config("Features", "use_youtube_downloader")))


@app.route("/videos")
def serve_video():
    """
    Serve local/downloaded video file to view/template
    :return: Video file
    """
    video_path = f'{utils.get_vid_save_path()}{filename}'
    return send_file(video_path)


@app.route("/upload/youtube/<video_id>")
def upload_youtube_id(video_id: str):
    """
    Upload a YouTube video directly from url with get parameter.
    :param video_id: The unique video id at the end of the YouTube video to be downloaded
    :return: Redirect to appropriate page after downloading or failing
    """
    youtube_url = f"https://www.youtube.com/watch?v={video_id}"
    return redirect(utils.download_youtube_video(youtube_url))


@app.route('/capture_at_timestamp', methods=['POST'])
def capture_at_timestamp():
    """
    Ajax endpoint for capturing code at current timestamp
    :return: Extracted and formatted code from timestamp
    """
    data = request.get_json()
    return ExtractText.extract_code_at_timestamp(f"{filename}", data.get('timestamp'))


@app.route("/send_to_ide", methods=["POST"])
def send_to_ide():
    """
    Ajax endpoint for sending code snippet to IDE
    :return: String indicating success or failure
    """
    code = request.get_json().get("code_snippet")
    unescaped_code = html.unescape(code)
    if utils.send_code_snippet_to_ide(filename, unescaped_code):
        return "success"
    else:
        return "fail"


@app.route("/update_video_data", methods=["POST"])
def update_video_data():
    """
    Ajax endpoint for updating video information in userdata
    :return: String indicating success or failure
    """
    data = request.get_json()
    if "progress" in data:
        utils.update_user_video_data(filename, progress=data["progress"])
        return "success"
    elif "capture" in data:
        utils.update_user_video_data(filename, capture=data["capture"])
        return "success"
    else:
        logging.error("No compatible data type to update")
        return {"error": "No compatible data type to update"}


@app.route("/upload_video", methods=["POST"])
def upload_video():
    """
    Upload a video from upload form to backend or from YouTube URL
    :return: Redirect to appropriate page
    """
    youtube_url = request.form.get("youtubeInput")
    file = request.files["localFileInput"]
    # TODO: Move this into separate function, too messy to have this logic in route method
    if file:
        if not os.path.exists(f"{utils.get_vid_save_path()}"):
            os.makedirs(f"{utils.get_vid_save_path()}")
        file.save(f"{utils.get_vid_save_path()}" + file.filename)
        global filename
        filename = file.filename
        file_hash = utils.hash_video_file(filename)
        if utils.file_already_exists(file_hash):
            return redirect(f"/play_video/{filename}")
        video_title = request.form.get("videoTitle")
        if video_title:
            utils.add_video_to_user_data(filename, video_title, file_hash)
        else:
            utils.add_video_to_user_data(filename, filename, file_hash)
        return redirect(f"/play_video/{filename}")
    elif youtube_url:
        return redirect(utils.download_youtube_video(youtube_url))
    logging.error("Failed to upload video file")
    return redirect("/upload")


@app.route("/play_video/<play_filename>")
def video(play_filename):
    """
    Returns video player view/template with specified video
    :param play_filename: Filename/video to play
    :return: Rendered template of video player
    """
    if utils.filename_exists_in_userdata(play_filename):
        global filename
        filename = play_filename
        return render_template("player.html", filename=filename, video_data=utils.get_video_data(filename))
    return redirect("/")


@app.route("/delete_video/<delete_filename>")
def delete_video(delete_filename):
    """
    Deletes a video from the userdata
    :param delete_filename: Filename/video to delete
    :return: Redirect to home page
    """
    if utils.filename_exists_in_userdata(delete_filename):
        utils.delete_video_from_userdata(delete_filename)
    return redirect("/")


@app.route("/update_settings", methods=['GET', 'POST'])
def update_settings():
    if request.method == "POST":
        new_values = utils.extract_form_values(request)
        utils.update_configuration(new_values)
        return redirect('/settings')
    current_settings = utils.get_current_settings()
    return render_template('settings.html', current_settings=current_settings)


@app.route('/reset-settings', methods=['POST'])
def reset_settings():
    print("Current working directory:", os.getcwd())
    # Delete the existing config.ini file
    if os.path.exists('config.ini'):
        os.remove('config.ini')
    shutil.copy('config.example.ini', 'config.ini')
    current_settings = utils.get_current_settings()
    return render_template('settings.html', current_settings=current_settings)


@app.route('/update_tesseract_path', methods=['GET', 'POST'])
def update_tesseract_path():
    global cancel_search_flag

    if request.method == 'POST' and request.form.get('cancel_search'):
        # Set the flag to indicate cancellation
        cancel_search_flag = True
        message = 'Tesseract search canceled.'
        current_settings = utils.get_current_settings()
        return render_template('settings.html', current_settings=current_settings, message=message)

    current_settings = utils.get_current_settings()
    if current_settings['AppSettings']['tesseract_executable'] == 'your_path_to_tesseract_here' \
            or current_settings['AppSettings']['tesseract_executable'] == '':
        file_pattern = 'tesseract.exe'
        for drive in range(65, 91):  # Drive letters 'A' to 'Z'
            drive_letter = chr(drive) + ':\\'
            if os.path.exists(drive_letter):
                for root, dirs, files in os.walk(drive_letter):
                    if cancel_search_flag:  # Check the cancellation flag
                        message = 'Tesseract search canceled.'
                        cancel_search_flag = False  # Reset the flag
                        return render_template('settings.html', current_settings=current_settings, message=message)

                    for file in glob.glob(os.path.join(root, file_pattern)):
                        file_path = file
                        utils.update_configuration({'AppSettings': {'tesseract_executable': file_path}})
                        message = 'Tesseract executable found and path updated successfully.'
                        current_settings = utils.get_current_settings()
                        return render_template('settings.html', current_settings=current_settings, message=message)

    message = 'Could not find tesseract executable. Please enter the path manually.'
    return render_template('settings.html', current_settings=current_settings, message=message)


if __name__ == "__main__":
    host = "localhost"
    port = 5000
    logging.basicConfig(filename="app.log", filemode="w", level=logging.DEBUG, format="%(levelname)s - %(message)s")
    print("[*] Starting OcrRoo Server")
    print(f"[*] OcrRoo Server running on http://{host}:{port}/")
    app.run(host=host, port=port)
else:
    logging.basicConfig(level=logging.DEBUG, format="%(levelname)s - %(message)s")

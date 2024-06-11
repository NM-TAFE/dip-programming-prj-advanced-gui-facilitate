/**
 * mediaControls.js
 *
 * This JavaScript file handles hotkeys and key bindings that are inside the video player view.
 */

// Parse DOM for needed elements
let videoPlayer = document.getElementById("videoPlayer");
let progressBar = document.getElementById("progressBar");
let currentTimestamp = document.getElementById("currentTimestamp");
let volumeSlider = document.getElementById("volumeSlider");
let muteButton = document.getElementById("muteButton");
let captureOutputContainer = document.getElementById("captureOutputContainer");
let mainCaptureButton = document.getElementById("mainCaptureButton");

// Add event listener to progress par in video player to update video position and timestamp on input
progressBar.addEventListener("input", () => {
    videoPlayer.currentTime = videoPlayer.duration * (progressBar.value / 100);
    currentTimestamp.innerHTML = formatTimestamp(videoPlayer.currentTime)
});

// Add event listener to video player to update progress bar, timestamp, and user data when time changes
videoPlayer.addEventListener("timeupdate", () => {
    progressBar.value = (videoPlayer.currentTime / videoPlayer.duration) * 100;
    currentTimestamp.innerHTML = formatTimestamp(videoPlayer.currentTime);
    sendProgressUpdate()
});

// Add event listener to volume slider of video player to update volume on input
volumeSlider.addEventListener("input", () => {
    videoPlayer.volume = volumeSlider.value;
});

// If video has been played before, open it to current timestamp
if (Number(progress) !== 0) {
    videoPlayer.currentTime = progress;
}

/**
 * Plays or pauses the video and updates play/pause button icon
 */
function playVideo() {
    let playButton = document.getElementById("playButton");
    if (videoPlayer.paused) {
        videoPlayer.play();
        playButton.classList.add("fa-pause");
        playButton.classList.remove("fa-play");
    } else {
        videoPlayer.pause();
        playButton.classList.remove("fa-pause");
        playButton.classList.add("fa-play");
    }
}

/**
 * Rewinds the current video position 5 seconds
 */
function rewindVideo() {
    if (videoPlayer.currentTime < 5) {
        videoPlayer.currentTime = 0;
    } else {
        videoPlayer.currentTime -= 5;
    }
}

/**
 * Skips the current video forward 5 seconds
 */
function skipVideo() {
    if (videoPlayer.duration - videoPlayer.currentTime > 5) {
        videoPlayer.currentTime += 5;
    } else {
        videoPlayer.currentTime = videoPlayer.duration;
    }
}

/**
 * Mutes the audio of the video and updates mute icon
 */
function muteVideo() {
    if (videoPlayer.volume === 0) {
        videoPlayer.volume = 1;
        volumeSlider.value = 1;
        muteButton.classList.add("fa-volume-high");
        muteButton.classList.remove("fa-volume-xmark");
    } else {
        videoPlayer.volume = 0;
        volumeSlider.value = 0;
        muteButton.classList.remove("fa-volume-high");
        muteButton.classList.add("fa-volume-xmark");
    }

}

/**
 * Sends progress update of video back to server
 */
function sendProgressUpdate() {
    $.ajax({
        url: "/update_video_data",
        type: "POST",
        data: JSON.stringify({"progress": videoPlayer.currentTime}),
        contentType: "application/json",
            success: function(response) {}
    });
}

/**
 * Send capture to server to update in userdata
 * @param timestamp Timestamp of code capture
 * @param capture_content Content of code capture
 */
function sendCaptureUpdate(timestamp, capture_content) {
    let rounded_timestamp = Math.round(timestamp);
    $.ajax({
        url: "/update_video_data",
        type: "POST",
        data: JSON.stringify({"capture": {
            "timestamp": rounded_timestamp,
            "capture_content": capture_content,
        }}),
        contentType: "application/json",
            success: function(response) {}
    });
}

/**
 * Sends request to server to capture code at current video timestamp
 */
function captureCode() {
    let captureTimestamp = videoPlayer.currentTime;
    mainCaptureButton.innerHTML = "<span><i class=\"fa-solid fa-circle-notch fa-spin mr-2\"></i>Analysing Frame</span>" +
        "<span class=\"text-xs my-1 text-gray-200\">(" + hotkeys["capture_code"] + ")</span>";
    $.ajax({
        url: "/capture_at_timestamp",
        type: "POST",
        data: JSON.stringify({"timestamp": captureTimestamp}),
        contentType: "application/json",
            success: function(response) {
                displayCapture(response, captureTimestamp);
                sendCaptureUpdate(captureTimestamp, response);
            }
    });
}

/**
 * Prints a capture to the output window
 * @param response Contents of code capture
 * @param timestamp Timestamp of  code capture
 */
function displayCapture(response, timestamp) {
    let captureOutput = document.createElement("div");
    captureOutput.classList.add("border", "border-gray-200", "mb-2", "p-2", "pt-0", "shadow-sm", "rounded-xl", "bg-white");
    let captureTimestamp = document.createElement("span");
    captureTimestamp.innerHTML = "Captured @ Timestamp: " + formatTimestamp(timestamp);
    let captureTitle = document.createElement("p");
    captureTitle.classList.add("text-gray-400", "text-xs", "flex", "justify-between", "border-b", "border-gray-200", "py-1");
    let captureBody = document.createElement("code");
    captureBody.id = "code_" + nextCodeId++;
    let copyThisCapture = document.createElement("button");
    copyThisCapture.innerHTML = "Open in IDE";
    copyThisCapture.classList.add("text-purple-600", "hover:cursor-pointer", "underline");
    copyThisCapture.onclick = () =>  openInIde(captureBody.id);
    captureTitle.appendChild(captureTimestamp);
    captureTitle.appendChild(copyThisCapture);
    captureOutput.appendChild(captureTitle);
    let captureBodyWrap = document.createElement("pre");
    captureBodyWrap.classList.add("overflow-x-auto");
    captureBody.classList.add("w-full", "whitespace-pre", "language-python", "text-xs");
    captureBody.contentEditable = "true";
    // Create a temporary div to decode HTML entities into regular text
    let tempDiv = document.createElement("div");
    tempDiv.innerHTML = response;
    // Get the decoded text from the temporary div
    let decodedText = tempDiv.textContent;
    captureBody.appendChild(document.createTextNode(decodedText));
    captureBodyWrap.appendChild(captureBody);
    captureOutput.appendChild(captureBodyWrap);
    let firstChild = captureOutputContainer.firstChild;
    captureOutputContainer.insertBefore(captureOutput, firstChild);
    mainCaptureButton.innerHTML = "<span><i class=\"fa-solid fa-expand mr-2\"></i>Capture Code on Frame</span>" +
        "<span class=\"text-xs my-1 text-gray-200\">(" + hotkeys["capture_code"] + ")</span>";
}

/**
 * Formats a timestamp from seconds to MM:SS
 * @param seconds Input timestamp in seconds
 * @returns {string} String of formatted timestamp
 */
function formatTimestamp(seconds) {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = Math.floor(seconds % 60);
    return `${String(minutes).padStart(2, '0')}:${String(remainingSeconds).padStart(2, '0')}`;
}

/**
 * Opens a capture in users preferred IDE
 * @param captureElementId (Optional) ID of capture output div to send to IDE, most recent capture will be sent
 * if ID, is not specified
 */
function openInIde(captureElementId) {
    let codeElement;
    if (typeof captureElementId === "undefined") {
        // If no elementId provided
        let firstChild = captureOutputContainer.firstElementChild;
        codeElement = firstChild.querySelector('code');
    } else {
        codeElement = document.getElementById(captureElementId);
    }
    // Send request to backend
    $.ajax({
        url: "/send_to_ide",
        type: "POST",
        data: JSON.stringify({"code_snippet": codeElement.innerHTML}),
        contentType: "application/json",
            success: function(response) {
                console.log("success");
            }
    });
}
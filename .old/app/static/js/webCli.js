/**
 * webCli.js
 *
 * This JavaScript file handles the web based command line interface and its associated functions
 */

// Parse DOM for needed elements
let webCliContainer = document.getElementById("webCliContainer");

let traverseResponsesIndex = 0;

// Global variables for auto completions
let autoCompleteArray = [];
let availableVideos = {};
getAvailableVideosFromServer();

// If webcli was open on previous page open on new page
if (localStorage.getItem("webCliOpen")  === "true") {
    openWebCli();
}

// Add key listener to the webcli to send commands with enter key
webCliContainer.addEventListener("keydown", function (event) {
    if (event.code === "Enter") {
        sendWebCliCommand();
    } else if (event.code === "ArrowUp") {
        traversePreviousCommands("up");
    } else if (event.code === "ArrowDown") {
        traversePreviousCommands("down");
    } else if (event.code === "Tab" && event.shiftKey) {
        event.preventDefault();
        traverseResponses("up");
    } else if (event.code === "Tab") {
        event.preventDefault();
        if (document.getElementById("webCliInput") === document.activeElement) {
            autoCompleteCommands();
        } else {
            traverseResponses("down");
        }
    } else if (event.code === "Space" || event.code === "Backspace") {
        autoCompleteArray = [];
    }
});

/**
 * Traverse through CLI responses/commands with tab and shift + tab keys
 * @param direction Direction to traverse the container
 */
function traverseResponses(direction) {
    let responseElements = webCliContainer.querySelectorAll(".cli-response, .cli-command");
    if (document.getElementById("webCliInput") === document.activeElement) {
        traverseResponsesIndex = responseElements.length - 2;
    }
    if (direction === "up") {
        if (traverseResponsesIndex !== 0) {
            traverseResponsesIndex--;
        }
    } else {
        traverseResponsesIndex++;
    }
    responseElements[traverseResponsesIndex].focus();
}

/**
 * Traverse through previous commands
 * @param direction Direction to traverse through commands
 */
function traversePreviousCommands(direction) {
    if (localStorage.getItem("previousCommands") != null) {
        let previousCommands = JSON.parse(localStorage.getItem("previousCommands") || []);
        let traverseIndex = parseInt(localStorage.getItem("traverseIndex"));
        if (direction === "up") {
            if (traverseIndex < previousCommands.length - 1) {
                traverseIndex++;
            }
        } else {
            if (traverseIndex > -1) {
                traverseIndex--;
            }
        }
        if (traverseIndex === -1) {
            document.getElementById("webCliInput").value = "";
        } else {
            document.getElementById("webCliInput").value = previousCommands[traverseIndex]["command"];
        }
        localStorage.setItem("traverseIndex", traverseIndex.toString());
    }
}

/**
 * Autocomplete commands when user presses tab
 */
function autoCompleteCommands() {
    // If autocomplete in progress
    if (autoCompleteArray.length !== 0) {
        document.getElementById("webCliInput").value = autoCompleteArray[0];
        autoCompleteArray.shift();
        return;
    }
    let currentCommand = document.getElementById("webCliInput").value;
    currentCommand = currentCommand.trim();
    if (currentCommand === "") {
        return;
    // Auto complete for navigate command
    } else if (currentCommand.includes("navigate")) {
       commandOptionAutoComplete("navigate" ,currentCommand);
       return;
    } else if (currentCommand.includes("play-video")) {
        commandOptionAutoComplete("play-video" ,currentCommand);
        return;
    }
    // Base auto completions
    let autoCompletions = ["navigate", "list-videos", "play-video", "capture", "open",
        "clear", "cls", "help"];
    let foundCompletions = [];
    for (let completion in autoCompletions) {
        if (autoCompletions[completion].indexOf(currentCommand) === 0) {
            foundCompletions.push(autoCompletions[completion])
        }
    }
    if (foundCompletions.length === 1) {
        document.getElementById("webCliInput").value = foundCompletions[0];
    } else if (foundCompletions.length !== 0) {
        foundCompletions.push(currentCommand);
        document.getElementById("webCliInput").value = foundCompletions[0];
        foundCompletions.shift();
        autoCompleteArray = foundCompletions;
    }
}

/**
 * Auto-completion for commands with multiple parameters
 * @param commandFor Command to do auto-complete for
 * @param currentCommand Current command in user input
 */
function commandOptionAutoComplete(commandFor, currentCommand) {
    let completions = [];
    if (commandFor === "navigate") {
        completions = ["navigate home", "navigate upload", "navigate collaborate", "navigate settings"];
    } else if (commandFor === "play-video") {
        completions = Object.values(availableVideos);
        for (let index in completions) {
            completions[index] = commandFor + " " + completions[index];
        }
    } else {
        return;
    }
    if (currentCommand === commandFor) {
        completions.push(currentCommand);
        document.getElementById("webCliInput").value = completions[0];
        completions.shift();
        autoCompleteArray = completions;
    } else {
        for (let index in completions) {
            if (completions[index].indexOf(currentCommand) === 0) {
                document.getElementById("webCliInput").value = completions[index];
                return;
            }
        }
    }
}

/**
 * Opens/shows the web command line interface on current page
 */
function openWebCli() {
    if (webCliContainer.classList.contains("hidden")) {
        populateWebCli();
        webCliContainer.classList.remove("hidden");
        localStorage.setItem("webCliOpen", "true");
        localStorage.setItem("traverseIndex", "-1");
        // Clear input after opening with hotkey
        setTimeout(() => {
            document.getElementById("webCliInput").value = "";
            document.getElementById("webCliInput").select();
        }, 50);
    } else {
        webCliContainer.classList.add("hidden");
        localStorage.setItem("webCliOpen", "false");
    }
}

/**
 * Get a list of videos available to play from the server
 */
function getAvailableVideosFromServer() {
    $.ajax({
        url: "/web_cli",
        type: "POST",
        data: JSON.stringify({"command": "available-videos"}),
        contentType: "application/json",
            success: function(response) {
                availableVideos = response;
            }
    });
}

/**
 * Sends command back to server with Ajax request
 */
function sendWebCliCommand() {
    let webCliInput = document.getElementById("webCliInput");
    addToLocalStore("previousCLI", "command", webCliInput.value);
    addToLocalStore("previousCommands", "command", webCliInput.value);
    $.ajax({
        url: "/web_cli",
        type: "POST",
        data: JSON.stringify({"command": webCliInput.value}),
        contentType: "application/json",
            success: function(response) {
                responseHandler(response);
            }
    });
}

/**
 * Add data to local storage on user device for persistence
 * @param key localStorage key to add to
 * @param type Type of message to add (command or response)
 * @param body Body of the message to add
 */
function addToLocalStore(key, type, body) {
    let previous = [];
    if (localStorage.getItem(key) !== null) {
        previous = JSON.parse(localStorage.getItem(key) || []);
    }
    let newCommandResponse = {
         [type]:body
    };
    if (key === "previousCommands") {
        previous.unshift(newCommandResponse);
    } else {
        previous.push(newCommandResponse);
    }
    localStorage.setItem(key, JSON.stringify(previous));
}

/**
 * Populate the CLI output after opening in new page
 */
function populateWebCli() {
    if (localStorage.getItem("previousCLI") !== null) {
        webCliContainer.innerHTML = "";
        let previous = JSON.parse(localStorage.getItem("previousCLI") || []);
        for (let item of previous) {
            if (item["command"]) {
                let commandContainer = document.createElement("div");
                commandContainer.classList.add("cli-command", "flex", "items-center");
                commandContainer.setAttribute("tabindex", "0");
                let commandLabel = document.createElement("p");
                commandLabel.classList.add("text-purple-300", "w-fit", "mr-1");
                commandLabel.innerHTML = "OcrRooWebCli>";
                commandContainer.append(commandLabel);
                let commandBody = document.createElement("p");
                commandBody.innerHTML = item["command"];
                commandContainer.append(commandBody);
                webCliContainer.append(commandContainer);
            } else {
                let responseOut = document.createElement("p");
                responseOut.innerHTML = item["response"];
                responseOut.classList.add("cli-response");
                responseOut.setAttribute("tabindex", "0");
                webCliContainer.append(responseOut);
            }
        }
        appendNewCliInput();
        forceScrollToBottom();
    }
}

/**
 * Handle the command line response from the server
 * @param response Response string from server
 */
function responseHandler(response) {
    if (response["redirect_page"]) {
        addToLocalStore("previousCLI","response", "Changed page to " + response["redirect_page"]);
        window.location.href = response["redirect_page"];
    } else if (response === "capture") {
        if (window.location.href.includes("/play_video/")) {
            captureCode();
            let timestamp = formatTimestamp(videoPlayer.currentTime);
            let responseString = "Capturing code at timestamp " + timestamp;
            addToLocalStore("previousCLI", "response", responseString);
            insertCliResponse(responseString);
        } else {
            createErrorResponse("You must be playing a video to capture code.")
        }
    } else if (response === "open") {
        if (window.location.href.includes("/play_video/")) {
            openInIde();
            let responseString = "Opening most recent capture in your IDE";
            addToLocalStore("previousCLI", "response", responseString);
            insertCliResponse(responseString);
        } else {
            createErrorResponse("You must be playing a video to open code captures in your IDE")
        }
    } else if (response["play_video"]) {
        let responseString = "Opening and playing video " + response["play_video"];
        addToLocalStore("previousCLI", "response", responseString);
        insertCliResponse(responseString);
        window.location.href = "/play_video/" + response["play_video"];
    } else {
        addToLocalStore("previousCLI", "response", response);
        insertCliResponse(response);
    }
}

/**
 * Display error response when user attempts to perform invalid action
 * @param errorString Error string to display
 */
function createErrorResponse(errorString) {
    let responseString = "<span class='text-red-500'>" + errorString + "</span>";
    addToLocalStore("previousCLI", "response", responseString);
    insertCliResponse(responseString);
}

/**
 * Inserts a response into the CLI output container
 * @param response Response string to add to container
 */
function insertCliResponse(response) {
    let responseOutput = document.createElement("p");
    responseOutput.classList.add("cli-response");
    responseOutput.setAttribute("tabindex", "0");
    let webCliInputOld = document.getElementById("webCliInput");
    webCliInputOld.setAttribute("readonly", "true");
    webCliInputOld.removeAttribute("id");
    webCliInputOld.classList.remove("cli-command");
    responseOutput.innerHTML = response;
    webCliContainer.append(responseOutput);
    // Clear command
    if (response === "clear") {
        webCliContainer.innerHTML = "";
        localStorage.removeItem("previousCLI");
    }
    appendNewCliInput();
    forceScrollToBottom();
}

/**
 * Appends a new input to the WebCli container
 */
function appendNewCliInput() {
    let newInputContainer = document.createElement("div");
    newInputContainer.classList.add("cli-command", "flex", "items-center");
    newInputContainer.setAttribute("tabindex", "0");
    let newLabel = document.createElement("label");
    newLabel.setAttribute("for", "webCliInput");
    newLabel.classList.add("text-purple-300", "w-fit", "mr-1");
    newLabel.innerHTML = "OcrRooWebCli>";
    newInputContainer.append(newLabel);
    let newInput = document.createElement("input");
    newInput.classList.add("cli-command", "flex-grow", "bg-transparent", "outline-none");
    newInput.setAttribute("id", "webCliInput");
    newInput.setAttribute("autocomplete", "off");
    newInputContainer.append(newInput);
    webCliContainer.append(newInputContainer);
}

/**
 * Force scroll of WebCli container to bottom
 */
function forceScrollToBottom() {
    setTimeout(() => {
      webCliContainer.scrollTop = webCliContainer.scrollHeight;
      document.getElementById("webCliInput").select();
    }, 100);
}
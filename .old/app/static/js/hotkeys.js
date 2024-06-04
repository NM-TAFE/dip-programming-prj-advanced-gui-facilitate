/**
 * hotkeys.js
 *
 * This JavaScript file handles the capture and routing of key bindings
 */

// Initialise empty object to hold current state of keys
const pressedKeys= {};

// Add event listener to whole document to check for key presses/keydown
document.addEventListener("keydown", function (event) {
    pressedKeys[event.code] = true;
    // Iterate through all hotkey bindings
    for (let action in hotkeys) {
        let actionHotkeys = hotkeys[action].split(",");
        let flag = true;
        // TODO: Change this to loop through pressedKeys and check that ONLY the actionHotkeys are pressed to prevent false positives.
        for (let key in actionHotkeys) {
            if (!pressedKeys[actionHotkeys[key]]) {
                flag = false;
            }
        }
        // Disable global hotkeys while WebCli open
        if (localStorage.getItem("webCliOpen")  === "false" || localStorage.getItem("webCliOpen") == null ||
            action === "open_web_cli") {
            if (flag) {
                let functionName = snakeToCamel(action);
                if (window[functionName] && typeof window[functionName] === "function") {
                    window[functionName]();
                }
            }
        }
    }
});

// Add event listener to whole document to check for key releases
document.addEventListener("keyup", function (event) {
    pressedKeys[event.code] = false;
});

/**
 * Convert a string from snake case to camel case for proper JS function naming conventions
 * @param str Input string in snake case
 * @returns {string} String formatted in camel case
 */
function snakeToCamel(str) {
  return str.replace(/_([a-z])/g, function (match, group) {
    return group.toUpperCase();
  });
}
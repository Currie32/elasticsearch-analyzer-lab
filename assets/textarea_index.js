document.addEventListener("DOMContentLoaded", function () {
    // Attach the event listener to all textarea elements dynamically rendered by Dash
    document.body.addEventListener("keydown", function (event) {
        // Check if the target is a textarea
        if (event.target.tagName === "TEXTAREA" && event.key === "Enter") {
            const textarea = event.target;
            const cursorPos = textarea.selectionStart;
            const textBefore = textarea.value.substring(0, cursorPos);
            const textAfter = textarea.value.substring(cursorPos);

            // Get the previous line's indentation
            const previousLine = textBefore.split("\n").pop();
            const indentMatch = previousLine.match(/^\s*/); // Match leading spaces or tabs
            const indentation = indentMatch ? indentMatch[0] : "";

            // Prevent default Enter behavior and insert the new line with the same indentation
            event.preventDefault();
            const newValue = textBefore + "\n" + indentation + textAfter;
            textarea.value = newValue;

            // Set the cursor to the correct position after the inserted indentation
            const newCursorPos = cursorPos + 1 + indentation.length;
            textarea.setSelectionRange(newCursorPos, newCursorPos);
        }
    });
});

document.addEventListener("DOMContentLoaded", function () {
    function createLineNumberingWrapper(textarea) {
        // Check if the textarea is already wrapped
        if (!textarea.parentElement.classList.contains("textarea-wrapper")) {
            // Create the wrapper and line number container
            const wrapper = document.createElement("div");
            wrapper.className = "textarea-wrapper";

            const lineNumbers = document.createElement("div");
            lineNumbers.className = "line-numbers";

            // Insert the wrapper and move the textarea into it
            textarea.parentNode.insertBefore(wrapper, textarea);
            wrapper.appendChild(lineNumbers);
            wrapper.appendChild(textarea);

            // Initialize and update line numbers
            updateLineNumbers(textarea, lineNumbers);

            // Attach event listeners
            textarea.addEventListener("input", () => updateLineNumbers(textarea, lineNumbers));
            textarea.addEventListener("scroll", () => {
                lineNumbers.scrollTop = textarea.scrollTop;
            });
        }
    }

    function updateLineNumbers(textarea, lineNumbers) {
        const lines = textarea.value.split("\n").length; // Count lines
        lineNumbers.innerHTML = ""; // Clear existing line numbers

        for (let i = 1; i <= lines; i++) {
            const lineNumber = document.createElement("div");
            lineNumber.textContent = i;
            lineNumbers.appendChild(lineNumber);
        }
    }

    // Automatically wrap all textareas on the page
    document.querySelectorAll("textarea").forEach((textarea) => {
        createLineNumberingWrapper(textarea);
    });
});

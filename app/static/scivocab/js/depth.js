function update(data) {
    if ("redirect" in data) {
        window.location.href = data["redirect"];
    }

    for (i = 0; i < 4; i++) {
        $("img#position_" + i.toString()).attr('src', data.filenames[i]);
    }

    document.getElementById("playButton").onclick = function() {
        new Audio(data.audio_file).play();
    }

    $("h1#header").text(data.current_target_word);
}

// When the page loads up for the first time (or is refreshed), the
// function registered in the callback below initializes the task with the
// first word in the sequence.
$(() => {
    $.getJSON("nextWord", {}, update);
    return false;
});

// The block of code below registers the 'update' function to be called
// every time the 'Next word' button is clicked.
$(document).on('click', '#nextWordButton', function() {
    const elements = document.getElementsByClassName("targetImage");
    let srcs = Array.from(elements).map((e) => e.src.split("/").slice(-1)[0]);

    // Check if there are duplicates
    if (srcs.includes("dv_placeholder.gif")) {
        alert("All the boxes must have images to continue.");
    }
    else {
        $.getJSON("nextWord", {response : JSON.stringify(srcs)}, update);

        // Clear the target image containers.
        Array.from(elements).forEach(e => { e.src = "/static/scivocab/dv_placeholder.gif"; });
    }

    return false;
});

// Define an event handler for dragstart events.
function dragstart_handler(ev) {
    ev.dataTransfer.setData(
        "text/plain",
        JSON.stringify({sourceElementId : ev.target.id, src : ev.target.src}));
    ev.dataTransfer.dropEffect = "move";
}

function dragover_handler(ev) {
    ev.preventDefault();
    ev.dataTransfer.dropEffect = "move";
}

function drop_handler(ev) {
    ev.preventDefault();
    const data = JSON.parse(ev.dataTransfer.getData("text/plain"));
    // If the drop target is an image, check whether it is empty. If it is
    // not empty, swap the images.
    const sourceElement = document.getElementById(data.sourceElementId);

    let targetElement;

    if (ev.target.tagName == "IMG") {
        targetElement = ev.target;
    }
    else {
        targetElement = ev.target.firstElementChild;
    }
    sourceElement.src = targetElement.getAttribute('src');
    targetElement.src = data.src;
}

$(() => {
    const elements = document.getElementsByClassName("sourceImageContainer");
    Array.from(elements).forEach(
        e => {
            e.addEventListener("dragstart", dragstart_handler, false); 
            e.addEventListener("dragover", dragover_handler, false);
            e.addEventListener("drop", drop_handler, false);
        });
});

$(() => {
    const elements = document.getElementsByClassName("targetImageContainer");
    Array.from(elements).forEach(e => {
        e.addEventListener("dragstart", dragstart_handler, false);
        e.addEventListener("dragover", dragover_handler, false);
        e.addEventListener("drop", drop_handler, false);
    });
});

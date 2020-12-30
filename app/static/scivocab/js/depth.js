let DRAGGED;

function update(data) {
    if ("redirect" in data) {
        window.location.href=data["redirect"];
    }
    for (i = 0; i < 4; i++) {
        $("img#position_"+ i.toString()).attr('src' , data.filenames[i]) ;
    }
    $("h1#header").text(data.current_target_word) ;
}


// When the page loads up for the first time (or is refreshed), the
// function registered in the callback below initializes the task with the
// first word in the sequence.
$(() => {
    $.getJSON("nextWord",
        {},
        update
    );
    return false;
});

// The block of code below registers the 'update' function to be called
// every time the 'Next word' button is clicked.
$(document).on('click', '#nextWordButton', function() {
    const elements = document.getElementsByClassName("targetImage");
    let srcs = Array.from(elements).map((e) => e.src);
    $.getJSON(
        "nextWord",
        {response: JSON.stringify(srcs)},
        update
    );

    // Clear the target image containers.
    Array.from(elements).forEach(e => { 
        e.src="";
    });

    return false;
});

// Define an event handler for dragstart events.
function dragstart_handler(ev) {
    ev.dataTransfer.setData("text/plain", ev.target.src);
    ev.dataTransfer.dropEffect = "move";
}


function dragover_handler(ev) {
    ev.preventDefault();
    ev.dataTransfer.dropEffect = "move";
}

function drop_handler(ev) {
    ev.preventDefault();
    const data = ev.dataTransfer.getData("text/plain");
    if (ev.target.tagName == "IMG") {
        ev.target.src = data;
    }
    else {
        ev.target.firstElementChild.src = data;
    }
}


$(() => {
    const elements = document.getElementsByClassName("sourceImageContainer");
    Array.from(elements).forEach(e => { 
        e.addEventListener("dragstart", dragstart_handler, false);
    });
});

$(() => {
    const elements = document.getElementsByClassName("targetImageContainer");
    Array.from(elements).forEach(e => { 
        e.addEventListener("dragover", dragover_handler, false);
        e.addEventListener("drop", drop_handler, false);
    });
});

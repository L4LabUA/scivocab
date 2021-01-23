function update(data) {
    if ("redirect" in data) {
        window.location.href=data["redirect"];
    }
    for (i = 0; i < 4; i++) {
        $("img#position_"+ i.toString()).attr('src' , data.filenames[i]) ;
    }
    document.getElementById("playButton").onclick = function() {
        new Audio(data.audio_file).play();
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
// every time an image is clicked.

$(document).on('click', 'img', function() {
    $.getJSON(
        "nextWord",
        {position: $(this).attr('id')},
        update
    );
    return false;
});

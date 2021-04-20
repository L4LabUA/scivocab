function update(data) {
    if ("redirect" in data) {
        window.location.href=data["redirect"];
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
// every time the 'Next' button is clicked.
$(document).on('click', '#nextWordButton', function() {
    definitionTextArea = document.getElementById("definition");
    if (definitionTextArea.value == "") {
        alert("You must enter a definition to proceed.");
    }
    else {
        $.getJSON("nextWord", {
            response : definitionTextArea.value}, update);
            definitionTextArea.value="";
    }
    return false;
});

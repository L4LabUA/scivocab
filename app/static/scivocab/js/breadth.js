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

//declares the varible so it can be used in multiple functions

var clicked_image_id=""; 


// sets clicked image id to varible
$(document).on('click', 'img', function() {
    clicked_image_id = $(this).attr('id');
    return false;
});


// The block of code below registers the 'update' function to be called when
// the next button is clicked; getJSON sends the data
$(document).on('click', '#nextWordButton', function() {
    if (clicked_image_id == "") {
        alert("Select an image to proceed");
    }
    else {
        $.getJSON("nextWord",
            {position : clicked_image_id},
            update
        );
    //empty string to reset imgage id
        clicked_image_id = "";
    }   
    return false;
});

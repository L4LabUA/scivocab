
function updateView() {
    window.location.href = "http://localhost:5000/breadth";
}

$(document).on('click', '#ContinueButton', function() {
    console.log("click works in json");
    updateView();
   return false;

});

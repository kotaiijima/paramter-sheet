    let frame_num = 0;
    let item_num = 0;
    let style_position = 0;

function true_button() {
    var button = document.getElementsByClassName("control_button");
    for (var i = 0; i < button.length; i++) {
        button[i].disabled = true;
    }
}

function false_button() {
    var button = document.getElementsByClassName("control_button");
    for (var i = 0; i < button.length; i++) {

        button[i].disabled = false;
    }
}
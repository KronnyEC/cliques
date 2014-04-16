var ws = new WebSocket ('ws://127.0.0.1:8765');
var token;
var chan;
var socket;


function socket_open(e) {
    console.log("Socket opened");
}

function socket_message(e) {
    var message = e.data;
    console.log('Received message ' + message);
    $('#chat_messages').append("<p>" + message + "</p><hr>");
    var element = document.getElementById("chat_messages");
    element.scrollTop = element.scrollHeight;
}

function socket_error(e) {
    var code = error.field;
    var description = error.description;
    console.log("Socket error", code, description);
}

function socket_close(e) {
    console.log("Socket closed");
}

function build_socket() {
    window.chan = new goog.appengine.Channel(window.token);
    window.socket = chan.open({
        onerror: socket_error,
        onmessage: socket_message,
        onopen: socket_open,
        onclose: socket_close
    });
}

function join_chat() {
    $.ajax({
        type: "POST",
        url: '/chat/join_chat/',
        success: function(result) {
            console.log('join success', result);
            window.token = result.token;
            build_socket();
        }
    });
}

function chat_message(msg) {
    console.log(window.socket, msg);
    window.socket.send(msg);
}

$(document).ready(function() {
    join_chat();

    // Bind chat_server keys
    var inputBox = document.getElementById("chat_box");

    inputBox.addEventListener("keydown", function(e) {
        if (!e) { var e = window.event; }

        //keyCode 13 is the enter/return button keyCode
        if (e.keyCode == 13) {
        // enter/return probably starts a new line by default
            e.preventDefault();
            console.log('enter');
            chat_message(inputBox.value);
            inputBox.value="";
        }
    });
    $("#chat_send").click(function() {
        console.log('enter');
        chat_message(inputBox.value);
        inputBox.value="";
    });
});
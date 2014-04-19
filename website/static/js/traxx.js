var token;
var chan;
var socket;


function socket_open(e) {
    console.log("Socket opened");
}

function socket_message(e) {
    var message = e.data;
    console.log("socket message", message, jQuery.parseJSON(message));
    add_chat_message(jQuery.parseJSON(message));
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

function add_chat_message(msg) {
    console.log("add chat message", msg);
    var message = urlify(msg[1]);
    var chat_messages = $('#chat_messages');
    $('#chat_messages').append("<p>" + msg[0] + ": " + message  + "</p><hr>");
    $('#chat_messages').scrollTop($('#chat_messages')[0].scrollHeight);
}

function join_chat() {
    $.ajax({
        type: "POST",
        url: '/chat/join_chat/',
        success: function(result) {
            console.log("result", result);
            window.token = result.token;
            build_socket();
            result.msgs.forEach(function(msg) {
                add_chat_message(msg)
            });
        }
    });
}

function chat_message(msg) {
    console.log(window.socket, msg);
    $.ajax({
        type: "POST",
        url: '/chat/message/',
        data: {'msg': msg}
    });
}

function urlify(text) {
    var expression = /[-a-zA-Z0-9@:%_\+.~#?&//=]{2,256}\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?/gi;
    var regex = new RegExp(expression);
    var t = 'www.google.com';
    return text.replace(regex, function(url) {
        return '<a href="' + url + '">' + url + '</a>';
    });
    // or alternatively
    // return text.replace(urlRegex, '<a href="$1">$1</a>')
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
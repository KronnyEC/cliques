var token;
var chan;
var socket;


function socket_open(e) {
    console.log("Socket opened");
}

function socket_message(e) {
    var message = e.data;
    console.log("socket message", message, jQuery.parseJSON(message));
    add_chat_message(jQuery.parseJSON(message), false);
}

function socket_error(e) {
    var code = e.field;
    var description = e.description;
    console.log("Socket error", code, description);
    // Token timed out, get a new one.
    if (code == 401 && description == "Token+timed+out.") {
        join_chat();
    }
}

function socket_close(e) {
    console.log("Socket closed", e);
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

function add_chat_message(msg, notify) {
    console.log("add chat message", msg);
    var message = urlify(msg[1]);
    var chat_messages = $('#chat_messages');
    $('#chat_messages').append("<p>" + msg[0] + ": " + message  + "</p><hr>");
    $('#chat_messages').scrollTop($('#chat_messages')[0].scrollHeight);
    if (notify) {
        chat_notify();
    }

}

function chat_notify() {
    document.title = '(1) Slashertraxx'
}


function add_chat_user(user) {
    $("#connected_users").append(user + ", ");
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
            $("#connected_users").empty();
            result.connected_users.forEach(function(user) {
                add_chat_user(user);
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

function check_in() {
    console.log('check in');
    $.ajax({
        type: "POST",
        url: '/chat/check_in/',
        success: function(result) {
            $("#connected_users").empty();
            result.connected_users.forEach(function(user) {
                add_chat_user(user);
            });
        }
    });
}

// Notifications
function get_notifications() {
    console.log('getting notifications');
    $.ajax({
        type: "GET",
        url: '/notifications/',
        success: function(results) {
            console.log('notifications', results);
            $("#notifications").empty();
            results.forEach(function(n) {
                add_notification(n)
            });
        },
        error: function(e) {
            console.log("note err", e);
        }
    });
}

function add_notification(n) {
    // n requires: text, level, link, created_at
    var template = '<div data-alert class="alert-box ' + n.level + ' radius"><a href="' + n.link + '">' + n.text + '</a><a href="#" class="close">&times;</a></div>';
    console.log(template);
    $("#notifications").append(template);
}

// End notifications

$(document).ready(function() {
    join_chat();
    get_notifications();
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

    // Clear notifications
    $(function() {
        $(window).focus(function() {
            window.title = 'SlasherTraxx';
            console.log('Focus');
        });

        $(window).blur(function() {
            console.log('Lost focus');
        });
    });

    // Check in every minute
    setInterval(function() {
        check_in();
    }, 60*1000);
});

$( window ).unload(function() {
    $.ajax({
        type: "POST",
        url: '/chat/leave_chat/',
        success: function(result) {
            console.log("left chat", result);
        }
    });
});
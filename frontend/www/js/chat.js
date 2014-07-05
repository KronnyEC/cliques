var token;
var chan;
var socket;
var backend_server = 'http://127.0.0.1:8080/api/v1';

// TODO: factory that joins chat. factory that gets chat messages. something
// that sends chat messgaes.


//function socket_open(e) {
//    console.log("Socket opened");
//}
//
//function socket_message(e) {
//    var message = e.data;
//    console.log("socket message", message, jQuery.parseJSON(message));
//    add_chat_message(jQuery.parseJSON(message), false);
//}
//
//function socket_error(e) {
//    var code = e.field;
//    var description = e.description;
//    console.log("Socket error", code, description);
//    // Token timed out, get a new one.
//    if (code == 401 && description == "Token+timed+out.") {
//        join_chat();
//    }
//}
//
//function socket_close(e) {
//    console.log("Socket closed", e);
//}
//
//function build_socket() {
//    window.chan = new goog.appengine.Channel(window.token);
//    window.socket = chan.open({
//        onerror: socket_error,
//        onmessage: socket_message,
//        onopen: socket_open,
//        onclose: socket_close
//    });
//}

//function add_chat_message(msg, notify) {
//    console.log("add chat message", msg);
//    var message = urlify(msg.message);
//    var chat_messages = $('#chat_messages');
//    $('#chat_messages').append("<div title='" + msg.sent + "'<p>" + msg.user + ": " + message  + "</p></div><hr>");
//    $('#chat_messages').scrollTop($('#chat_messages')[0].scrollHeight);
//    if (notify) {
//        chat_notify();
//    }
//
//}

function chat_notify() {
    document.title = '(1) Slashertraxx'
}


//function add_chat_user(user) {
//    $("#connected_users").append(user + ", ");
//}


//function join_chat() {
//    if (token != undefined) {
//
//    } else {
//        $.ajax({
//            type: "POST",
//            url: backend_server + '/chat/sessions/',
//            success: function(result) {
//                console.log("result", result);
//                window.token = result.session_key;
//                build_socket();
//            }
//        });
//    }
//    get_messages();
//}
//
//function get_messages() {
//    $.ajax({
//        type: "GET",
//        url: backend_server + '/chat/messages/',
//        success: function(result) {
//            result.results.forEach(function(msg) {
//                add_chat_message(msg)
//            });
//            $("#connected_users").empty();
//            result.connected_users.forEach(function(user) {
//                add_chat_user(user);
//            });
//        }
//    });
//}
//
//function chat_message(msg) {
//    console.log(window.socket, msg);
//    $.ajax({
//        type: "POST",
//        url: backend_server + '/chat/message/',
//        data: {'msg': msg}
//    });
//}

function urlify(text) {
    var expression = /(^|\s)((https?:\/\/)?[\w-]+(\.[\w-]+)+\.?(:\d+)?(\/\S*)?)/gi;

    var regex = new RegExp(expression);
    var t = 'www.google.com';
    return text.replace(regex, function(url) {
        return '<a href="' + url + '">' + url + '</a>';
    });
    // or alternatively
    // return text.replace(urlRegex, '<a href="$1">$1</a>')
}
//
//function check_in() {
//    console.log('check in');
//    $.ajax({
//        type: "POST",
//        url: backend_server + '/chat/check_in/',
//        success: function(result) {
//            $("#connected_users").empty();
//            result.connected_users.forEach(function(user) {
//                add_chat_user(user);
//            });
//        }
//    });
//}

function chat_box_init() {
//    Check in every minute
//    setInterval(function() {
//        check_in();
//    }, 60*1000);

    $(document).on('click', '.notification_container', function(e) {
        var notification_id = e.target.id.split('_')[1];
        clear_notification(notification_id);
    });
}

$( window ).unload(function() {
    $.ajax({
        type: "POST",
        url: backend_server + '/chat/leave_chat/',
        success: function(result) {
            console.log("left chat", result);
        }
    });
});
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
    var expression = /(^|\s)((https?:\/\/)?[\w-]+(\.[\w-]+)+\.?(:\d+)?(\/\S*)?)/gi;

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
            console.log('notifications', results, results.length);
            $("#notifications").empty();
            if (results.results.length > 0) {
                $('#notifications_button').removeClass('inactive');
                $('#notifications_button').addClass('active');
            }
            results.results.forEach(function(n) {
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
    var template = '<li class="notification_container" id="notification_' + n.id + '_container"><a href="' + n.link + '" id="notification_' + n.id + '" >' + n.text + '</a></li></div>';
    console.log(template);
    $("#notifications").append(template);
}

function clear_notification(notification_id) {
    $.ajax({
        type: "DELETE",
        url: '/notifications/' + notification_id + '/',
        success: function(results) {
            var notification_selector = '#notification_' + notification_id;
            $(notification_selector).remove();
        },
        error: function(e) {
            console.log("notification delete err", e);
        }
    });
}

// End notifications

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}

$(document).ready(function() {
    join_chat();
    get_notifications();

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
            }
        }
    });


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

    $(document).on('click', '.notification_container', function(e) {
        var notification_id = e.target.id.split('_')[1];
//        console.log();
        clear_notification(notification_id);
    });
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
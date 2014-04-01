var ws = new WebSocket ('ws://127.0.0.1:8765');

ws.onerror = function (e) {
    console.log ('Error with WebSocket uid: ' + e.target.uid);
};

ws.onopen = function (e) {
    ws.send('test');
};

ws.onmessage = function(e) {
    var message = e.data
    $('#chat_messages').append("<p>" + message + "</p>");
    console.log('Received message ' + e.data);
};
ws.onerror = function (e) {
    console.log('< pipe1 error : ' + e.data);
};
ws.onclose = function (e) {
    console.log('connection closed!');
};

$(document).ready(function() {
    $("#chat_send").click(function() {
        ws.send($("#chat_box").val());
        $("#chat_box").val('');
    });

    // Bind chat keys
    var inputBox = document.getElementById("chat_box");

    inputBox.addEventListener("keydown", function(e) {
        if (!e) { var e = window.event; }

        //keyCode 13 is the enter/return button keyCode
        if (e.keyCode == 13) {
        // enter/return probably starts a new line by default
            e.preventDefault();
            console.log('enter');
            ws.send(inputBox.value);
            inputBox.value="";
        }
    });
});
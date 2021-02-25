function show_messages(){
    document.getElementById('message_board').style.display = 'block'
}

var socket = io.connect('https://127.0.0.1:5000');
    socket.on('connect', function() {
        socket.send('User has connected!');
});
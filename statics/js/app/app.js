(function (window, $, SockJS, undef) {
    'use strict';

    var connection = new SockJS('http://' + window.location.host + '/sock');

    connection.onopen = function (e) {
        console.log('opened');
    };

    connection.onclose = function (e) {
        console.log('closed');
    };

    connection.onerror = function () {
        console.log('error');
    };

    connection.onmessage = function (msg) {
        var data = JSON.parse(msg.data);

        switch (data[0]) {
        case 'chatmessage':
            var $row = $('<span>');
            $row.text(data[1] + ': ' + data[2]);
            $('#Chat').append('<br/>').append($row);
            break;
        case 'players':
            $('#ChatParticipants').empty().append(data[1].join(', '));
            break;
        }
    };

    window.connection = connection;

    var $confirmNameButton = $('#ConfirmNameButton'),
        $nameInput = $('#PlayerNameInput'),
        $chatSendButton = $('#SendButton'),
        $chatInput = $('#ChatInput');

    $confirmNameButton.on('click', function (e) {
        e.preventDefault();
        var name = $nameInput.val(),
            msg;
        if (name) {
            msg = JSON.stringify(['playername', name]);
            connection.send(msg);
            $('body').removeClass('modal-visible');
        }
    });

    $chatSendButton.on('click', function (e) {
        e.preventDefault();
        var msg = $chatInput.val();
        if (msg) {
            msg = JSON.stringify(['chatmessage', msg]);
            connection.send(msg);
        }
        $chatInput.val('');
    });

}(this, this.jQuery, this.SockJS));

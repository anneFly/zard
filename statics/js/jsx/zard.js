(function (window, $, SockJS, undef) {
    'use strict';


    var handler = {
        'message': function (msg) {
            $('#message').text(msg);
        },
        'error': function (msg) {
            $('#message').text(msg);
        },
        'trump': function (trump) {
            $('#trump').text(trump);
        },
        'hand': function (hand) {
            $('#hand').text(hand);
        }
    };



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
        console.log(data[0], data[1]);

        handler[data[0]](data[1]);

    };

    window.connection = connection;


    // $('#start').on('click', function (e) {
    //     e.preventDefault();
    //
    //     var msg = JSON.stringify(['start']);
    //
    //     connection.send(msg)
    // });
    //
    window.connection.send(JSON.stringify(['start']));


}(this, this.jQuery, this.SockJS));

(function (window, $, SockJS, undef) {
    'use strict';

    var connection = new SockJS('http://' + window.location.host + '/sock');

    connection.onopen = function (e) {
        console.log('opened');
        this.send('Hello my friend');
    };

    connection.onclose = function (e) {
        console.log('closed');
    };

    connection.onerror = function () {
        console.log('error');
    };

    connection.onmessage = function (msg) {
        $('#MainContent').append('<br/>' + msg.data);
    };

    window.connection = connection;

}(this, this.jQuery, this.SockJS));

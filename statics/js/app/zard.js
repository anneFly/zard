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

        // TODO
    };

    // debug only
    window.connection = connection;

}(this, this.jQuery, this.SockJS));

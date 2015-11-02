var StateStore = require('./store.jsx');
var run = require('./app.jsx')

var store = new StateStore();
run('test', store);

var connection = new SockJS('http://' + window.location.host + '/sock');

connection.onopen = function (e) {
    store.updateState('connection', connection);
};

connection.onclose = function (e) {
    console.log('closed');
};

connection.onerror = function () {
    console.log('error');
};

connection.onmessage = function (msg) {
    var data = JSON.parse(msg.data);
    var command = data[0];

    switch (command) {
    case 'error':
        alert(data[1].msg);
        break;
    default:
        store.updateState(command, data[1]);
        break;
    }
    console.log(data);
};

// debug only
window.connection = connection;

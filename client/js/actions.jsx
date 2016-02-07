var Actions = function (connection) {
    this.connection = connection;
};

Actions.prototype = {
    createGame: function (args) {
        this.connection.send(JSON.stringify(['createGame', args]));
    },
    joinGame: function (args) {
        this.connection.send(JSON.stringify(['joinGame', args]));
    },
    leaveGame: function () {
        this.connection.send(JSON.stringify(['leaveGame']));
    },
    rename: function (args) {
        this.connection.send(JSON.stringify(['rename', args]))
    }
};


module.exports = Actions;

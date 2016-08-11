class Actions {
    constructor (connection) {
        this.connection = connection;
    }
    createGame (args) {
        this.connection.send(JSON.stringify(['createGame', args]));
    }
    joinGame (args) {
        this.connection.send(JSON.stringify(['joinGame', args]));
    }
    leaveGame () {
        this.connection.send(JSON.stringify(['leaveGame']));
    }
    rename (args) {
        this.connection.send(JSON.stringify(['rename', args]))
    }
}


module.exports = Actions;

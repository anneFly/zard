var React = require('react');
var ReactDOM = require('react-dom');
var StateStore = require('./store.jsx');
var UserView = require('./views/user.jsx').UserView;
var LobbyView = require('./views/lobby.jsx').LobbyView;
var GameView = require('./views/game.jsx').GameView;


var store = new StateStore();


var AppView = React.createClass({
    getInitialState: function() {
        return {};
    },
    componentDidMount: function () {
        this.props.store.onUpdate(this.setState.bind(this));
        this.setupConnection();
        this.setActions();
    },
    setupConnection: function () {
        var that = this;
        var connection = new SockJS('http://' + window.location.host + '/sock');
        connection.onopen = function (e) {
            that.connection = connection;
        };
        connection.onclose = function (e) {
            console.log('closed');
        };
        connection.onerror = function () {
            console.log('error');
        };
        connection.onmessage = function (msg) {
            var message = JSON.parse(msg.data);
            var command = message[0];
            var data = message[1];

            switch (command) {
            case 'error':
                alert(data.msg);
                break;
            default:
                that.props.store.updateState(command, data);
                break;
            }
            console.log(message);
        };
    },
    setActions: function () {
        this.actions = {
            onCreateGame: this.onCreateGame,
            onJoinGame: this.onJoinGame,
            onLeaveGame: this.onLeaveGame,
            onRename: this.onRename
        }
    },
    onCreateGame: function (args) {
        this.connection.send(JSON.stringify(['createGame', args]));
    },
    onJoinGame: function (e) {
        var $btn = $(e.currentTarget);
        var gameId = $btn.data('game-id');
        this.connection.send(JSON.stringify(['joinGame', {id: gameId}]));
    },
    onLeaveGame: function (e) {
        this.connection.send(JSON.stringify(['leaveGame']));
    },
    onRename: function (args) {
        this.connection.send(JSON.stringify(['rename', args]))
    },
    render: function () {
        var lobby, game, user;
        if (this.state.userState) {
            if (!this.state.userState.userName) {
               user = <UserView actions={this.actions} />
            }
            else if (this.state.userState.inGame) {
                game = <GameView {...this.state.gameState} actions={this.actions} />
            }
            else {
                lobby = <LobbyView {...this.state.lobby} actions={this.actions} />
            }
        }
        return (
            <div>
                {user}
                {lobby}
                {game}
            </div>
        );
    }
});


window.addEventListener('load', function () {
    ReactDOM.render(
        <AppView store={store}/>,
        document.getElementById('app')
    );
});

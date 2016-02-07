var React = require('react');
var ReactDOM = require('react-dom');
var StateStore = require('./store.jsx');
var Actions = require('./actions.jsx');
var UserView = require('./views/user.jsx').UserView;
var LobbyView = require('./views/lobby.jsx').LobbyView;
var GameView = require('./views/game.jsx').GameView;


var store = new StateStore();


var AppView = React.createClass({
    getInitialState: function() {
        return {
            userState: {},
            lobbyState: {},
            gameState: {},
        };
    },
    componentDidMount: function () {
        this.props.store.onUpdate(this.setState.bind(this));
        this.setupConnection();
        this.setActions();
    },
    setupConnection: function () {
        var that = this;
        var connection = new SockJS('http://' + window.location.host + '/sock');
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
        this.connection = connection;
    },
    setActions: function () {
        this.actions = new Actions(this.connection);
    },
    render: function () {
        var lobbyView, gameView, userView;

        userView = <UserView {...this.state.userState} actions={this.actions} />
        if (this.state.userState.userName) {
            if (this.state.userState.inGame) {
                gameView = <GameView {...this.state.gameState} userState={this.state.userState} actions={this.actions} />
            }
            else {
                lobbyView = <LobbyView {...this.state.lobbyState} actions={this.actions} />
            }
        }
        return (
            <div>
                {userView}
                {lobbyView}
                {gameView}
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

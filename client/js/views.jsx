var React = require('react');


var CreateGameMaskView = React.createClass({
    render: function () {
        var state = this.props.state;
        var actions = this.props.actions;
        var onCreateGame = actions['onCreateGame'];
        return (
            <div>
                <form>
                    <input type="text" name="gameName" placeholder="game name" />
                    <select name="gameSize">
                        <option value="3">3 Players</option>
                        <option value="4">4 Players</option>
                        <option value="5">5 Players</option>
                        <option value="6">6 Players</option>
                    </select>
                    <button type="button" onClick={onCreateGame}>Create</button>
                </form>
            </div>
        );
    }
});

var LobbyView = React.createClass({
    getInitialState: function() {
        return {createGameMaskIsShown: false};
    },
    toggleGameMask: function () {
        this.setState({createGameMaskIsShown: !this.state.createGameMaskIsShown});
    },
    render: function () {
        var data = this.props.data;
        var numUsers, numGames, createGameMask;
        if (data.users) {
            numUsers = data.users.length;
        }
        if (data.games) {
            numGames = data.games.length;
        }
        if (this.state.createGameMaskIsShown) {
            createGameMask = <CreateGameMaskView actions={this.props.actions} />
        }
        return (
            <div>
                Number of users: {numUsers}
                <br/>
                Number of games: {numGames}
                <hr/>
                <button type="button" onClick={this.toggleGameMask}>Create Game</button>
                {createGameMask}
            </div>
        );
    }
});

var GameView = React.createClass({
    render: function () {
        var state = this.props.data

        return (
            <div>
                Game: {state.name}
            </div>
        );
    }
});


module.exports.AppView = React.createClass({
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
        };
    },
    setActions: function () {
        this.actions = {
            onCreateGame: this.onCreateGame
        }
    },
    onCreateGame: function (e) {
        var $btn = $(e.currentTarget);
        var $form = $btn.closest('form');
        var name = $form.find('[name=gameName]').val();
        var size = $form.find('[name=gameSize]').val();
        this.connection.send(JSON.stringify(['createGame', {name: name, 'size': size}]));
    },
    render: function () {
        var lobby, game;
        if (this.state.gameState) {
            game = <GameView data={this.state.gameState} />
        }
        else if (this.state.lobby) {
            lobby = <LobbyView data={this.state.lobby} actions={this.actions}/>
        }
        return (
            <div>
                {lobby}
                {game}
            </div>
        );
    }
});

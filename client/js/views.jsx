var React = require('react');


var CreateGameMaskView = React.createClass({
    onCreateGame: function (e) {
        var $btn = $(e.currentTarget);
        var $form = $btn.closest('form');
        var name = $form.find('[name=gameName]').val();
        var size = $form.find('[name=gameSize]').val();
        this.props.connection.send(JSON.stringify(['createGame', {name: name, 'size': size}]));
    },
    render: function () {
        var state = this.props.state;
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
                    <button type="button" onClick={this.onCreateGame}>Create</button>
                </form>
            </div>
        );
    }
});

var GameListItemView = React.createClass({
    onJoinGame: function (e) {
        var $btn = $(e.currentTarget);
        var gameId = $btn.data('game-id');
        this.props.connection.send(JSON.stringify(['joinGame', {id: gameId}]));
    },
    render: function() {
        var data = this.props.data;
        return (
            <li>
                {data.name} ({data.users.length}/{data.size})
                <button type="button" data-game-id={data.id} onClick={this.onJoinGame}>Join Game</button>
            </li>
        );
    }
});

var GameListView = React.createClass({
    render: function() {
        var connection = this.props.connection;
        return (
            <ul>
            {this.props.data.map(function(result) {
                return <GameListItemView key={result.id} data={result} connection={connection} />;
            })}
            </ul>
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
            gameListView = <GameListView data={data.games} connection={this.props.connection} />;
        }
        if (this.state.createGameMaskIsShown) {
            createGameMask = <CreateGameMaskView connection={this.props.connection} />;
        }
        return (
            <div>
                Number of users: {numUsers}
                <br/>
                {gameListView}
                <hr/>
                <button type="button" onClick={this.toggleGameMask}>Create Game</button>
                {createGameMask}
            </div>
        );
    }
});

var GameView = React.createClass({
    render: function () {
        var data = this.props.data;

        return (
            <div>
                You joined Game: {data.name}
                <br/>
                Status: {data.status}
                <br/>
                Players: {data.players}
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
    render: function () {
        var lobby, game;
        if (this.state.gameState) {
            game = <GameView data={this.state.gameState} connection={this.connection} />
        }
        else if (this.state.lobby) {
            lobby = <LobbyView data={this.state.lobby} connection={this.connection} />
        }
        return (
            <div>
                {lobby}
                {game}
            </div>
        );
    }
});

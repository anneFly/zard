var React = require('react');

var LobbyView = React.createClass({
    render: function () {
        var state = this.props.data;
        var actions = this.props.actions;
        var onCreateGame = actions['onCreateGame'];
        var numUsers, numGames;
        if (state.users) {
            numUsers = state.users.length;
        }
        if (state.games) {
            numGames = state.games.length;
        }
        return (
            <div>
                Number of users: {numUsers}
                <br/>
                Number of games: {numGames}
                <hr/>
                <button type="button" onClick={onCreateGame}>Create Game</button>
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
        this.setActions();
    },
    setActions: function () {
        this.actions = {
            'onCreateGame': this.onCreateGame
        }
    },
    onCreateGame: function (e) {
        this.state.connection.send(JSON.stringify(['createGame', {name: 'my first game', 'size': 3}]));
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

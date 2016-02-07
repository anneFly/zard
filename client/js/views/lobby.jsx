var React = require('react');
var LinkedStateMixin = require('react-addons-linked-state-mixin');


var CreateGameMaskView = React.createClass({
    mixins: [LinkedStateMixin],
    getInitialState: function () {
        return {
            gameName: '',
            gameSize: 3
        };
    },
    onCreateGame: function (event) {
        this.props.actions.createGame({
            name: this.state.gameName,
            size: this.state.gameSize
        });
    },
    render: function () {
        return (
            <div>
                <form>
                    <input type="text" placeholder="game name" valueLink={this.linkState('gameName')} />
                    <select valueLink={this.linkState('gameSize')}>
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
        this.props.actions.joinGame({
            id: this.props.game.id
        });
    },
    render: function() {
        var game = this.props.game;
        return (
            <li>
                {game.name} ({game.users.length}/{game.size})
                <button type="button" onClick={this.onJoinGame}>Join Game</button>
            </li>
        );
    }
});

var GameListView = React.createClass({
    render: function() {
        return (
            <ul>
            {this.props.games.map(function(result) {
                return <GameListItemView key={result.id} game={result} actions={this.props.actions} />;
            }.bind(this))}
            </ul>
        );
    }
});

module.exports.LobbyView = React.createClass({
    getInitialState: function() {
        return {createGameMaskIsShown: false};
    },
    toggleGameMask: function () {
        this.setState({createGameMaskIsShown: !this.state.createGameMaskIsShown});
    },
    render: function () {
        var createGameMask;
        if (this.props.games) {
            gameListView = <GameListView {...this.props} actions={this.props.actions} />;
        }
        if (this.state.createGameMaskIsShown) {
            createGameMask = <CreateGameMaskView actions={this.props.actions} />;
        }
        return (
            <div>
                Number of users: {this.props.users.length}
                <br/>
                {gameListView}
                <hr/>
                <button type="button" onClick={this.toggleGameMask}>Create Game</button>
                {createGameMask}
            </div>
        );
    }
});

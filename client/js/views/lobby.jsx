const React = require('react');


class CreateGameMaskView extends React.Component {
    constructor (props) {
        super(props);
        this.state = {
            gameName: '',
            gameSize: 3
        }
    }
    onCreateGame (event) {
        const gameName = this.refs.nameInput.value;
        const gameSize = this.refs.sizeInput.value;
        this.props.actions.createGame({
            name: gameName,
            size: gameSize,
        });
    }
    render () {
        return (
            <div>
                <form>
                    <input type="text" placeholder="game name" ref='nameInput' />
                    <select ref='sizeInput'>
                        <option value="3">3 Players</option>
                        <option value="4">4 Players</option>
                        <option value="5">5 Players</option>
                        <option value="6">6 Players</option>
                    </select>
                    <button type="button" onClick={this.onCreateGame.bind(this)}>Create</button>
                </form>
            </div>
        );
    }
}

class GameListItemView extends React.Component {
    onJoinGame (e) {
        this.props.actions.joinGame({
            id: this.props.game.id
        });
    }
    render () {
        let game = this.props.game;
        return (
            <li>
                {game.name} ({game.users.length}/{game.size})
                <button type="button" onClick={this.onJoinGame.bind(this)}>Join Game</button>
            </li>
        );
    }
}

class GameListView extends React.Component {
    render () {
        return (
            <ul>
            {this.props.games.map((result) => {
                return <GameListItemView key={result.id} game={result} actions={this.props.actions} />;
            })}
            </ul>
        );
    }
}

class LobbyView extends React.Component {
    constructor (props) {
        super(props);
        this.state = {createGameMaskIsShown: false};
    }
    toggleGameMask (event) {
        this.setState({createGameMaskIsShown: !this.state.createGameMaskIsShown});
    }
    render () {
        let gameListView, createGameMask;
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
                <button type="button" onClick={this.toggleGameMask.bind(this)}>Create Game</button>
                {createGameMask}
            </div>
        );
    }
}


module.exports = {
    LobbyView,
}

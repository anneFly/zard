var React = require('react');


class GuessingView extends React.Component {
    renderGuesses () {
        const rows = [];
        for (playerName in this.props.guesses) {
            rows.push([playerName, this.props.guesses[playerName]]);
        }
        return (
            <div>
                <hr/>
                Currently Guessing: {this.props.activePlayer}<br/>
                <table>
                    {rows.map(function (row) {
                        return (<tr key={row[0]}><td>row[0]</td><td>row[1]</td></tr>)
                    })}
                </table>
            </div>
        );
    }
    renderGuessForm () {
        if (this.props.activePlayer == this.props.userState.userName) {
            return (<div>todo gamemask</div>)
        }
    }
    render () {
        return (
            <div>
                {this.renderGuesses()}
                {this.renderGuessForm()}
            </div>
        );
    }
}

class PlayingView extends React.Component {
    render () {
        return (<div>todo playing</div>);
    }
}

class EndView extends React.Component {
    render () {
        return (<div>todo end</div>);
    }
}

class GameView extends React.Component {
    onLeaveGame (e) {
        this.props.actions.leaveGame();
    }
    render () {
        let guessingView, playingView, endView;
        if (this.props.state == 'GUESSING') {
            guessingView = <GuessingView {...this.props} />
        } else if (this.props.state == 'PLAYING') {
            playingView = <PlayingView {...this.props} />
        } else if (this.props.state == 'END') {
            endView = <EndView {...this.props} />
        }

        return (
            <div>
                You joined Game: {this.props.name}
                <br/>
                Status: {this.props.state}
                <br/>
                Users: {this.props.users.join(', ')}
                <button type="button" onClick={this.onLeaveGame.bind(this)}>leave game</button>
                {guessingView}
                {playingView}
                {endView}
            </div>
        );
    }
}


module.exports = {
    GameView,
}

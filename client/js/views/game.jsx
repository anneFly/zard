var React = require('react');


var GuessingView = React.createClass({
    renderGuesses: function () {
        var rows = [];
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
    },
    renderGuessMask: function () {
        if (this.props.activePlayer == this.props.userState.userName) {
            return (<div>todo gamemask</div>)
        }
    },
    render: function () {
        return (
            <div>
                {this.renderGuesses()}
                {this.renderGuessMask()}
            </div>
        );
    }
});

var PlayingView = React.createClass({
    render: function () {
        return (<div>todo playing</div>);
    }
});

var EndView = React.createClass({
    render: function () {
        return (<div>todo end</div>);
    }
});

module.exports.GameView = React.createClass({
    onLeaveGame: function (e) {
        this.props.actions.leaveGame();
    },
    render: function () {
        var guessingView, playingView, endView;
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
                <button type="button" onClick={this.onLeaveGame}>leave game</button>
                {guessingView}
                {playingView}
                {endView}
            </div>
        );
    }
});

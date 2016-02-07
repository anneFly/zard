var React = require('react');


module.exports.GameView = React.createClass({
    onLeaveGame: function (e) {
        this.props.actions.leaveGame();
    },
    render: function () {
        return (
            <div>
                You joined Game: {this.props.name}
                <br/>
                Status: {this.props.state}
                <br/>
                Users: {this.props.users.join(', ')}
                <button type="button" onClick={this.onLeaveGame}>leave game</button>
            </div>
        );
    }
});

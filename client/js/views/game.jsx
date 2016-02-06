var React = require('react');


module.exports.GameView = React.createClass({
    render: function () {
        var actions = this.props.actions;

        return (
            <div>
                You joined Game: {this.props.name}
                <br/>
                Status: {this.props.state}
                <br/>
                Users: {this.props.users.join(', ')}
                <button type="button" onClick={actions.onLeaveGame}>leave game</button>
            </div>
        );
    }
});

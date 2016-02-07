var React = require('react');
var LinkedStateMixin = require('react-addons-linked-state-mixin');


module.exports.UserView = React.createClass({
    mixins: [LinkedStateMixin],
    getInitialState: function () {
        return {
            userName: this.props.userName,
        };
    },
    onRename: function (event) {
        this.props.actions.rename({
            name: this.state.userName
        });
    },
    render: function () {
        if (this.props.userName) {
            return (
                <div>Hello {this.props.userName}</div>
            )
        } else {
            return (
                <div>
                    Please enter a user name:
                    <input type="text" valueLink={this.linkState('userName')}/>
                    <button type="button" onClick={this.onRename}>Submit</button>
                </div>
            );
        }
    }
});

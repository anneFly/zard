var React = require('react');
var LinkedStateMixin = require('react-addons-linked-state-mixin');


module.exports.UserView = React.createClass({
    mixins: [LinkedStateMixin],
    getInitialState: function () {
        return {
            userName: '',
        };
    },
    rename: function (event) {
        this.props.actions.onRename({
            name: this.state.userName
        });
    },
    render: function () {
        return (
            <div>
                Please enter a user name:
                <input type="text" valueLink={this.linkState('userName')}/>
                <button type="button" onClick={this.rename}>Submit</button>
            </div>
        );
    }
});

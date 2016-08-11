const React = require('react');



class UserView extends React.Component {
    constructor (props) {
        super(props);
    }
    onRename (event) {
        const name = this.refs.input.value;
        this.props.actions.rename({
            name: name
        });
    }
    render () {
        if (this.props.userName) {
            return (
                <div>Hello {this.props.userName}</div>
            )
        } else {
            return (
                <div>
                    Please enter a user name:
                    <input type="text" ref='input' />
                    <button type="button" onClick={this.onRename.bind(this)}>Submit</button>
                </div>
            );
        }
    }
}


module.exports = {
    UserView
}

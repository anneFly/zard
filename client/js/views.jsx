var React = require('react');

module.exports.AppView = React.createClass({
  componentWillMount: function () {
    this.props.store.onUpdate(this.render.bind(this));
  },
  componentWillUnmount: function () {
    // TODO
    // this.prop.store.off(...)
  },
  render: function () {
    return (
      <div>
        Hello world!
      </div>
    );
  }
})

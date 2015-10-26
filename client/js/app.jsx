var React = require('react');
var ReactDOM = require('react-dom');
var views = require('./views.jsx');
var StateStore = require('./store.jsx');


module.exports = function (elId) {
  var store = new StateStore();
  window.addEventListener('load', function () {
    ReactDOM.render(
        <views.AppView store={store}/>,
        document.getElementById(elId)
    )
  });
};

var React = require('react');
var ReactDOM = require('react-dom');
var StateStore = require('./store.jsx');
var views = require('./views.jsx');


var store = new StateStore();

window.addEventListener('load', function () {
    ReactDOM.render(
        <views.AppView store={store}/>,
        document.getElementById('app')
    );
});

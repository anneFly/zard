var React = require('react');
var ReactDOM = require('react-dom');
var views = require('./views.jsx');


module.exports = function (elId, store) {
    window.addEventListener('load', function () {
        ReactDOM.render(
            <views.AppView store={store}/>,
            document.getElementById(elId)
        );
    });
};

var StateStore = function () {
    this._callback = undefined;
    this.state = {};
}

StateStore.prototype = {
    updateState: function (stateType, state) {
        this.state[stateType] = state;
        if (this._callback) {
            this._callback(this.state);
        }
    },
    onUpdate: function (cb) {
        this._callback = cb;
    }
};


module.exports = StateStore;

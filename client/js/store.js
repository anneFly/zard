class StateStore {
    constructor () {
        this._callback = undefined;
        this.state = {};
    }
    updateState (stateType, state) {
        this.state[stateType] = state;
        if (this._callback) {
            this._callback(this.state);
        }
    }
    onUpdate (cb) {
        this._callback = cb;
    }
}


module.exports = StateStore;

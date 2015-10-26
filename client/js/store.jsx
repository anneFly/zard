var StateStore = function () {
  this._callbacks = [];
  this._state = null;
}

StateStore.prototype = {
  update: function (state) {
    this._state = state;
    this.trigger();
  },
  state: function () {
    return this._state
  },
  onUpdate: function (cb) {
    this._callbacks.push(cb)
  },
  trigger: function () {
    this._callbacks.each(function () {
      fn.call(this, this.state);
    });
  }
}


module.exports = StateStore

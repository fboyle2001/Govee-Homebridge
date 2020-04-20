<<<<<<< HEAD
=======
var http = require('http');
>>>>>>> a5714045ec030483ea3954c827b96adb264374f9
var Service, Characteristic;

module.exports = function(homebridge) {
  console.log("homebridge API version: " + homebridge.version);

  // Service and Characteristic are from hap-nodejs
  Service = homebridge.hap.Service;
  Characteristic = homebridge.hap.Characteristic;

  homebridge.registerAccessory("homebridge-govee-switch", "GoveeSwitch", goveeSwitch);
}

<<<<<<< HEAD
const request = require('request');
const url = require('url');

=======
>>>>>>> a5714045ec030483ea3954c827b96adb264374f9
goveeSwitch.prototype = {
  getServices: function() {
    let informationService = new Service.AccessoryInformation();
    informationService.setCharacteristic(Characteristic.Manufacturer, "Govee")
      .setCharacteristic(Characteristic.Model, "H6129")
      .setCharacteristic(Characteristic.SerialNumber, "123-456-789");

    let switchService = new Service.Switch("Govee Switch");
    switchService.getCharacteristic(Characteristic.On)
      .on("get", this.getSwitchOnCharacteristic.bind(this))
      .on("set", this.setSwitchOnCharacteristic.bind(this));

    this.informationService = informationService;
    this.switchService = switchService;
    return [informationService, switchService];
  }
}
<<<<<<< HEAD

function goveeSwitch(log, config) {
  this.log = log;
  this.getUrl = url.parse(config['getUrl']);
  this.postUrl = url.parse(config['postUrl']);
}

goveeSwitch.prototype = {
  getSwitchOnCharacteristic: function (next) {
    const me = this;
    request({
      url: me.getUrl,
      method: 'GET',
    },
    function (error, response, body) {
      if (error) {
        me.log('STATUS: ' + response.statusCode);
        me.log(error.message);
        return next(error);
      }
      return next(null, body.currentState);
    });
  },

  setSwitchOnCharacteristic: function (on, next) {
    const me = this;
    request({
      url: me.postUrl,
      body: {'targetState': on},
      method: 'POST',
      headers: {'Content-type': 'application/json'}
    },
    function (error, response) {
      if (error) {
        me.log('STATUS: ' + response.statusCode);
        me.log(error.message);
        return next(error);
      }
      return next();
    });
  }
};
=======
>>>>>>> a5714045ec030483ea3954c827b96adb264374f9
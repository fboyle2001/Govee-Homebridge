var Service, Characteristic;

module.exports = function(homebridge) {
  console.log("homebridge API version: " + homebridge.version);

  // Service and Characteristic are from hap-nodejs
  Service = homebridge.hap.Service;
  Characteristic = homebridge.hap.Characteristic;

  homebridge.registerAccessory("homebridge-govee-switch", "GoveeSwitch", goveeSwitch);
}

const url = require('url');
const got = require('got');

function goveeLEDStrip(log, config) {
  this.log = log;

  this.lightService = new Service.Lightbulb("Finlay's LED");
  this.lightService.getCharacteristic(Characteristic.On);
}

goveeLEDStrip.prototype = {
  isLightOn: function(next) {
    got("http://localhost:5000/status").then(response => {
      this.log.log(response.body);
      return next(null, response.body.data.status)
    }).catch(error => {
      this.log.log(error.response.body);
      return next(error);
    });
  },

  toggleLight: function (next) {
    got("http://localhost:5000/toggle").then(response => {

    }).catch(error => {

    });
  }
}

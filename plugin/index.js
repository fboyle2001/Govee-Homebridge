var Service, Characteristic;

module.exports = function(homebridge) {
  console.log("homebridge API version: " + homebridge.version);

  // Service and Characteristic are from hap-nodejs
  Service = homebridge.hap.Service;
  Characteristic = homebridge.hap.Characteristic;

  homebridge.registerAccessory("homebridge-govee-led", "LED Strip", goveeLEDStrip);
}

const url = require('url');
const got = require('got');

function goveeLEDStrip(log, config) {
  this.log = log;

  this.informationService = new Service.AccessoryInformation();
  this.informationService.setCharacteristic(Characteristic.Manufacturer, "Govee");
  this.informationService.setCharacteristic(Characteristic.Model, "H6182");
  this.informationService.setCharacteristic(Characteristic.SerialNumber, "6182-0001");

  this.lightService = new Service.Lightbulb("LED Strip");
  this.lightService.getCharacteristic(Characteristic.On)
  .on("get", this.isLightOn.bind(this))
  .on("set", this.toggleLight.bind(this));
  this.lightService.getCharacteristic(Characteristic.Brightness)
  .on("get", this.getBrightness.bind(this))
  .on("set", this.setBrightness.bind(this));
  this.lightService.getCharacteristic(Characteristic.Hue)
  .on("get", this.getHue.bind(this))
  .on("set", this.setHue.bind(this));
  this.lightService.getCharacteristic(Characteristic.Saturation)
  .on("get", this.getSaturation.bind(this))
  .on("set", this.setSaturation.bind(this));
}

goveeLEDStrip.prototype = {
  isLightOn: function(next) {
    return next(null, this.on);
  },

  toggleLight: function(value, next) {
    if(value == false) {
      console.log("Turning light off");
      (async() => {
        got("http://10.0.0.20:5000/api/update/off?mac=A4:C1:38:A0:7B:19").then(response => {
          response = JSON.parse(response.body);
          console.log("OFF LIGHT: ", response);
          this.on = value;
          return next(null);
        }).catch(error => {
          console.log(error);
          return next(error);
        });
      })();
    } else {
      console.log("Turning light on");
      (async() => {
        got("http://10.0.0.20:5000/api/update/on?mac=A4:C1:38:A0:7B:19").then(response => {
          response = JSON.parse(response.body);
          console.log("ON LIGHT: ", response);
          this.on = value;
          return next(null);
        }).catch(error => {
          console.log(error);
          return next(error);
        });
      })();
    }
  },

  getBrightness: function(next) {
    return next(null, this.brightness);
  },

  setBrightness: function(value, next) {
    (async() => {
      got("http://10.0.0.20:5000/api/update/brightness?mac=A4:C1:38:A0:7B:19&brightness=" + value).then(response => {
        response = JSON.parse(response.body);
        console.log("SET BRIGHTNESS: ", response);
        this.brightness = brightness;
        return next(null);
      }).catch(error => {
        console.log(error);
        return next(error);
      });
    })();
  },

  getHue: function(next) {
    console.log("GET HUE WAS CALLED");
    return next(null, this.hue);
  },

  setHue: function(value, next) {
    (async() => {
      got("http://10.0.0.20:5000/api/update/hs?mac=A4:C1:38:A0:7B:19&hue=" + value + "&saturation=" + this.saturation).then(response => {
        response = JSON.parse(response.body);
        console.log("SET HUE: ", response);
        this.hue = value;
        return next(null);
      }).catch(error => {
        console.log(error);
        return next(error);
      });
    })();
    return next(null);
  },

  getSaturation: function(next) {
    console.log("GET SATURATION WAS CALLED");
    return next(null, this.saturation);
  },

  setSaturation: function(value, next) {
    this.saturation = value;
    return next(null);
  },

  getServices: function() {
    return [this.informationService, this.lightService];
  }
}

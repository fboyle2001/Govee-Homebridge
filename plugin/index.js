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

  this.initialise();
}

goveeLEDStrip.prototype = {
  initialise: function() {
    (async() => {
      got("http://10.0.0.20:5000/register?mac=A4:C1:38:A0:7B:19&name=LED%20Strip");
    })();
    this.toggleLight(false, function (error, value) {});
  },

  isLightOn: function(next) {
    (async() => {
      got("http://10.0.0.20:5000/status?device=A4:C1:38:A0:7B:19").then(response => {
        response = JSON.parse(response.body);
        console.log("IS LIGHT ON: ", response);
        return next(null, response.data.status);
      }).catch(error => {
        console.log(error.response.body);
        return next(error);
      });
    })();
  },

  toggleLight: function(value, next) {
    if(value == false) {
      console.log("Turning light off");
      (async() => {
        got("http://10.0.0.20:5000/off?device=A4:C1:38:A0:7B:19").then(response => {
          response = JSON.parse(response.body);
          console.log("OFF LIGHT: ", response);
          return next(null);
        }).catch(error => {
          console.log(error.response.body);
          return next(error);
        });
      })();
    } else {
      console.log("Turning light on");
      (async() => {
        got("http://10.0.0.20:5000/on?device=A4:C1:38:A0:7B:19").then(response => {
          response = JSON.parse(response.body);
          console.log("ON LIGHT: ", response);
          return next(null);
        }).catch(error => {
          console.log(error.response.body);
          return next(error);
        });
      })();
    }
  },

  getBrightness: function(next) {
    (async() => {
      got("http://10.0.0.20:5000/get_brightness?device=A4:C1:38:A0:7B:19").then(response => {
        response = JSON.parse(response.body);
        console.log("GET BRIGHTNESS: ", response);
        return next(null, response.data.brightness);
      }).catch(error => {
        console.log(error.response.body);
        return next(error);
      });
    })();
  },

  setBrightness: function(value, next) {
    int_value = Math.round((value / 100) * 255);

    if(int_value > 255) {
      int_value = 255;
    } else if(int_value < 0) {
      int_value = 0;
    }

    (async() => {
      got("http://10.0.0.20:5000/brightness?device=A4:C1:38:A0:7B:19&level=" + int_value).then(response => {
        response = JSON.parse(response.body);
        console.log("SET BRIGHTNESS: ", response);
        return next(null);
      }).catch(error => {
        console.log(error.response.body);
        return next(error);
      });
    })();
  },

  getHue: function(next) {
    console.log("GET HUE WAS CALLED");
    return next(0, null);
  },

  setHue: function(value, next) {
    console.log("SET HUE WAS CALLED");
    console.log("PROVIDED VALUE WAS: ", value);
    return next(null);
  },

  getSaturation: function(next) {
    console.log("GET SATURATION WAS CALLED");
    return next(0, null);
  },

  setSaturation: function(value, next) {
    console.log("SET SATURATION WAS CALLED");
    console.log("PROVIDED VALUE WAS: ", value);
    return next(null);
  },

  getServices: function() {
    return [this.informationService, this.lightService];
  }
}

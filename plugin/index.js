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
    got("http://10.0.0.20:5000/status?device=A4:C1:38:A0:7B:19").then(response => {
      response = JSON.parse(response.body)
      console.log("IS LIGHT ON: ", response);

      if(response.status.code == 504) {
        //retry
        console.log("Error, need to retry");
      }

      return next(null, response.data.status);
    }).catch(error => {
      this.log.log(error.response.body);
      return next(error);
    });
  },

  toggleLight: function(value, next) {
    this.log.log("Toggle Light value: " + value);
    got("http://10.0.0.20:5000/toggle?device=A4:C1:38:A0:7B:19").then(response => {
      response = JSON.parse(response.body);
      console.log("TOGGLE LIGHT: ", response);

      if(response.status.code == 504) {
        //retry
        console.log("Error, need to retry");
      }

      return next(null);
    }).catch(error => {
      this.log.log(error.response.body);
      return next(error);
    });
  },

  getBrightness: function(next) {
    got("http://10.0.0.20:5000/get_brightness?device=A4:C1:38:A0:7B:19").then(response => {
      response = JSON.parse(response.body);
      console.log("GET BRIGHTNESS: ", response);

      if(response.status.code == 504) {
        //retry
        console.log("Error, need to retry");
      }

      return next(null, response.data.brightness);
    }).catch(error => {
      this.log.log(error.response.body);
      return next(error);
    });
  },

  setBrightness: function(value, next) {
    int_value = Math.round((value / 100) * 255);

    if(int_value > 255) {
      int_value = 255;
    } else if(int_value < 0) {
      int_value = 0;
    }

    got("http://10.0.0.20:5000/brightness?device=A4:C1:38:A0:7B:19&level=" + int_value).then(response => {
      response = JSON.parse(response.body);
      console.log("SET BRIGHTNESS: ", response);

      if(response.status.code == 504) {
        //retry
        console.log("Error, need to retry");
      }

      return next(null);
    }).catch(error => {
      this.log.log(error.response.body);
      return next(error);
    });
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

var http = require('http');
var Service, Characteristic;

module.exports = function(homebridge) {
  console.log("homebridge API version: " + homebridge.version);

  // Service and Characteristic are from hap-nodejs
  Service = homebridge.hap.Service;
  Characteristic = homebridge.hap.Characteristic;

  homebridge.registerAccessory("homebridge-govee-switch", "GoveeSwitch", goveeSwitch);
}

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

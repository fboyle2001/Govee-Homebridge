const got = require('got');

(async() => {
  const response = await got("http://10.0.0.20:5000/on?device=A4:C1:38:A0:7B:19");
  console.log(response.body);
})();
(async() => {
  const response = await got("http://10.0.0.20:5000/brightness?device=A4:C1:38:A0:7B:19&level=255");
  console.log(response.body);
})();

const got = require('got');

console.log("test")
got("http://127.0.0.1:5000/colour?device=a&r=200").then(response => {
  response = JSON.parse(response.body)
  console.log("response")
  console.log(response.status.code)
}).catch(error => {
  console.log("error")
  console.log(error)
});

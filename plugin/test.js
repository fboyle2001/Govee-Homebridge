const got = require('got');

let status_code = 0;

function attempt(url) {
  return ;
}

got("http://10.0.0.20:5000/error_generate/500").then(a => {
  a = JSON.parse(a.body);
  console.log(a.status.code);
}).catch(error => {
  console.log("Errored #1");
  console.log(error);
});

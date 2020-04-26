const got = require('got');

let status_code = 0;

function attempt(url) {
  return ;
}

got("http://10.0.0.20:5000/on?device=A4:C1:38:A0:7B:19").then(a => {
  a = JSON.parse(a.body);
  console.log(a.status.code);
  if(a.status.code == 200) {
    return;
  }
  console.log("Single failure");
  got("http://10.0.0.20:5000/on?device=A4:C1:38:A0:7B:19").then(b => {
    b = JSON.parse(b.body);
    console.log(b.status.code);
    if(b.status.code == 200) {
      return;
    }
    console.log("Double failure");
  }).catch(error => {
    console.log("Errored #2");
    console.log(error);
  });
}).catch(error => {
  console.log("Errored #1");
  console.log(error);
});

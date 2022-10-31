var host = "localhost:8484";
var socket; // the websocket
var connected = false;
var msg = "pas de serveur"

function setup() {
  createCanvas(300, 200);
  socket = new WebSocket("ws://" + host);
  socket.onopen = sendIntro;
  socket.onmessage = readMessage;
  socket.onclose = fin
  frameRate(30);

}

function draw() {
  background("#2307AF");
  fill(255);
  text(msg,30,30);
  if (connected) socket.send("1"); // envoi bidon ... à réfléchir
  else {} // to do for reconnect
}

function sendIntro() {
  socket.send("GO"); // envoi bidon ... à réfléchir
}

function readMessage(event) {
  msg = event.data;
  connected = true;
}

function fin(){
  msg = "Pas de serveur"
  connected = false
}

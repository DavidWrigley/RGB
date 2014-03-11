var server = require("./server");
var net = require("net");
var Websocketserver = require("ws").Server;

var mywebsocketserver = new Websocketserver({port: 11223});
var mysocket = new net.Socket();
var myserver = new net.createServer();
var globalws = null;

/***************************
	websocket communcation
****************************/

mywebsocketserver.on('connection', function(ws) {
	globalws = ws;
	ws.on('message', function(data) {
		console.log("websocket got: " + String(data));
		ws.send("something from node.js");
	});

	ws.on('close', function() {
		console.log("websocket closed");
		globalws = null;
	});
});

/*******************************
	unix (python) communcation
*******************************/

myserver.listen(8080, 'localhost');

myserver.on('connection', function(socket) {
	console.log("got connection: " + socket.remoteAddress + " " + socket.remotePort);

	socket.on('data', function(data) {
		console.log("got data: " + data);
		if (globalws === null) {
			console.log("External Websocket not connected!");
		} else {
			globalws.send(String(data));
		}
	});
});

myserver.on('close', function() {
	console.log("socket closed");
});

server.start();
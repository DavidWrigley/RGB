var http = require("http"),
	fs = require('fs');

function start() {

	function onRequest(request, response) {
		console.log("got request");
		response.writeHead(200, {'Content-Type': 'text/plane'});
		response.write("hello");
		response.end();
	}

	http.createServer(onRequest).listen(8888);

	console.log("server has started");
}

exports.start = start;
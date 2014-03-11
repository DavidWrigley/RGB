#!/usr/local/bin/node

var http    = require('http'),
    io      = require('socket.io'),
    fs      = require('fs'),
    util    = require('util'),
    sys     = require("sys"),
    path    = require("path");
    fileBase = '';

    process.argv.forEach(function(val, index, array) {
        console.log(index + ': ' + val);
    });

    var port = 27017;

    console.log("Port Number: " + port);

        http = http.createServer(handler);
        http.listen(port);
        io = io.listen(http);

        io.set('log level', 1); // reduce logging

        function handler(request, response) {

            var filePath = fileBase + request.url;
            if (filePath == fileBase + '/')
                filePath = fileBase + '/index.html';

            console.log('request starting...'+request.url);

            var extname = path.extname(filePath);
            var contentType = 'text/html';
            switch (extname) {
                case '.js':
                    contentType = 'text/javascript';
                    break;
                case '.css':
                    contentType = 'text/css';
                    break;
            }

            path.exists(filePath, function(exists) {
                if (exists) {
                    fs.readFile(filePath, function(error, content) {
                        if (error) {
                            response.writeHead(500);
                            response.end();
                        } else {
                            response.writeHead(200, { 'Content-Type': contentType });
                            response.end(content, 'utf-8');
                        }
                    });
                } else {
                    response.writeHead(404);
                    response.end();
                }
            });
        };

        io.sockets.on('connection',function(socket){
		socket.on('msg',function(data){
		var value=data.toString();
		var splitIndex= value.indexOf(' ');
		var topic=value.substring(0, splitIndex);
		var payload=value.substring(splitIndex);
		socket.emit('user message',{topic:topic, payload:payload});
		});

		process.stdin.on('data', function(data) {
		var value=data.toString();
		var splitIndex= value.indexOf(' ');
		var topic=value.substring(0, splitIndex);
		var payload=value.substring(splitIndex);
		socket.emit('user message',{topic:topic, payload:payload});
	});
});
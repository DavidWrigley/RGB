function getFingerprintingPercentageDone (numSamples, arrayCnt) {

	var percDone = ""
			
	for (var nodeId in arrayCnt) {

		if ((arrayCnt[nodeId] / numSamples) * 100 < 100)
			percDone += nodeId + ": " + Math.round( (arrayCnt[nodeId] / numSamples) * 100 ) + " ";
		else 
			percDone += nodeId + ": 100 ";

		console.log("percDone[nodeId] = %d", percDone);
	}

	return percDone;
}

//######################################################################
//io Socket Code.
// creating a new websocket to keep the content updated without any AJAX request

io.sockets.on( 'connection', function ( socket ) {

	iosocket = socket;

	socket.on('startFingerprinting', function (data) {

	    startFingerprinting = true;
	   	
	   	fingBuilding = data.building;
	   	fingRoom = data.room;
	   	fingMac = data.mac;
		fingX = data.x;
		fingY = data.y;

	    console.log('Starting a Fingerprinting session.. building:%s, room:%s, mac:%s, x:%d, y:%d', 
	    	data.building, data.room, data.mac, data.x, data.y);
	});
});


var express 	= require('express'),
	app 		= express(),
	http  		= require('http').Server(app),
	client 		= require('socket.io').listen(http),
	mongoose	= require('mongoose'),
	bodyParser	= require('body-parser');


var port = 2000;

app.use(bodyParser.json());

http.listen(port, function(){
	console.log("Listening at port " + port);
});


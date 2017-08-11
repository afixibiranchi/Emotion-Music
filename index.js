var express 	= require('express'),
	app 		= express(),
	http  		= require('http').Server(app),
	client 		= require('socket.io').listen(http),
	mongoose	= require('mongoose'),
	bodyParser	= require('body-parser');


var port = 3333;

http.listen(port, function(){
	console.log("Listening at port " + port);
});


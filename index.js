var express 	= require('express'),
	app 		= express(),
	http  		= require('http').Server(app),
	client 		= require('socket.io').listen(http),
	mongoose	= require('mongoose'),
	bodyParser	= require('body-parser');


var port = 2222;

http.listen(port, function(){
	console.log("Listening at port " + port);
});


app.use(bodyParser.json());

app.get('/music', function(req,res){
	res.sendFile('/e.mp3', {root:__dirname});
});

// app.use('/node_modules', express.static(__dirname + "/node_modules"));

client.on('connection', function(socket){

	console.log("Connection made");

	socket.on("DataFromPy", function(data){
		console.log(data);
	});

	var data = {
		name : "Ugenteraan",
		emotion : "Angry"
	};

	client.emit("data4android", data);

});

app.post('/trying', function(req,res){

	console.log(req.body);

});
	

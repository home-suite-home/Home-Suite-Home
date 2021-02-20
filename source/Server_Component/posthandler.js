// Accept http POST requests, print contentes to console
// then push to mongo db database


const http = require('http');
const MongoClient = require('mongodb').MongoClient;
const assert = require('assert');


// Server IP and port
const hostname = 'localhost';
const port = 3000;


// Connection URL
const url = 'mongodb://localhost:27017';

// Database Name
const dbName = 'sensorsdb';

// Create a new MongoClient
const client = new MongoClient(url);
const connection = client.connect();



const server = http.createServer((req, res) => {
  
  if( req.method === 'POST') {
		let body = '';
  	req.on('data', chunk => {
  		body += chunk;
  	})
  	req.on('end', () => {
  	
  	var doc = JSON.parse(body);
  	
  	const connect = connection;
  	connect.then(() => {
  	var doc = JSON.parse(body);
  	const db = client.db(dbName);
		const collection = db.collection('sensors');
		
  	collection.insertOne(doc, 
		function(err, res) {
			if (err) throw err;
			console.log("Document successfully inserted!")
			
			});
		});
  	
  	console.log(JSON.parse(body));
  	res.end();
  	})
  }
});

client.close();

server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});

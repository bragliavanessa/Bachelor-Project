/**
 * A small node app to showcase the application.
 *
 * By default will use the implicit grant (aka client-side) oauth flow.
 * To try out the authorization code (aka server-side) flow copy
 * bower-components/mendeley-javascript-sdk/examples/oauth-config.auth-code.js.dist
 * to application/oauth-config.js filling in your client ID and secret.
 */

/* jshint camelcase: false */
'use strict';

var config = require('./oauth-config');
var express = require('express');

var app = express();
var url = 'http://localhost';
var port = 8111;

// Directories examples/ and lib/ always served statically
app.use('/application', express.static(__dirname));
app.use('/dist', express.static(__dirname + '/../bower_components/mendeley-javascript-sdk/dist'));

// Require oauth-app for auth code flow if configured for a "code" reponse type
if (config.responseType === 'code') {
	config.redirectUri = url + ':' + port + '/oauth/token-exchange';
	require('./oauth-app')(app, config);
}

// Error handling
app.use(function(error, req, res, next) {
	if (error) {
		console.error(error.stack);
		res.status(500).send('Something broke!');
	}
});

// Run the server
var server = app.listen(port, function() {
	console.info('App running, using "' + config.responseType + '" oauth flow');
	console.info('Test the app at ' + url + ':' + server.address().port + '/application/');

});
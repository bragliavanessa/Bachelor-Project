// var sdk = require('@mendeley/api');
// var api = sdk({
// 	authFlow: sdk.Auth.clientCredentialsFlow({
// 		clientId: 5242,
// 		clientSecret: "UlDkJVL7KmVBVCnY",
// 		redirectUri: "http://localhost:5000/oauth"
// 	})
// });
//
// api.documents.list().then(function(docs) {
//
// 	console.log('Success!');
// 	console.log(docs);
//
// }).catch(function(response) {
//
// 	console.log('Failed!');
// 	console.log('Status:', response);
//
// });
'use strict';

var getDocs = function() {
	MendeleySDK.API.documents
		.list()
		.done(function(docs) {
			console.log(docs);
		})
		.fail(errorHandler);
}
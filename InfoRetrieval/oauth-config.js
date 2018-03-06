/**
 * This is an example of the oauth config required to use the implict grant
 * flow aka the client-side flow.
 *
 * This requires no server-to-server interaction at all. The trade-off is you
 * only get access for a limited time and there is no refresh token - after that
 * time expires the user has to log-in again.
 *
 * To use this config copy it to oauth-config.js, fill in your clientId and
 * make sure it is loaded via a script tag in examples/index.html.
 */

try {
	window.oauthImplicitGrantConfig = {
		clientId: 5242, // <-- Add your client id here!
		responseType: 'token'
	};
} catch (e) {
	console.info('Client side oauth config ignored');
	if (module.exports) {
		module.exports = {
			responseType: 'token'
		};
	}
}
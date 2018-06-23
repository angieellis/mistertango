'use strict';
var CryptoJS = require("crypto-js");
var myArgs = require('optimist').argv;

var API_SECRET = myArgs._[0];
var _nonce = myArgs._[1];
var _data = myArgs._[2];
var _command_url = myArgs._[3];

function makeSignature(nonce, data, command_url)
{
	const hashstring = nonce + data;
	const hashed = CryptoJS.SHA256(hashstring).toString(CryptoJS.enc.Latin1);
 	const encoded = CryptoJS.enc.Latin1.parse(command_url + hashed);

 	return CryptoJS.HmacSHA512(encoded, API_SECRET).toString(CryptoJS.enc.Base64);
}

console.log(makeSignature(_nonce, _data, _command_url));
// console.log(myArgs._[0]);
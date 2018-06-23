'use strict';
var us = require('microseconds');
var request = require("request");
var base64 = require('base-64');
var CryptoJS = require("crypto-js");
var querystring = require('querystring');

var API_URL = 'https://api.mistertango.com:8445';
var API_KEY = '25bb9957-7552-11e8-9885-0218ad050e37';
var API_SECRET = 'b87efe69ffa5953';
var API_USER = 'goo.filip.stojanovic@gmail.com';


function getBalance() {
  return new Promise(function(resolve, reject) 
  {
	var command_url = '/v1/transaction/getBalance';
	var full_url = API_URL + command_url;
	var nonce = getNonce();

	var data = 'username=' + convertUsername(API_USER) + '&nonce='+nonce;
 	const signature = makeSignature(nonce, data, command_url);

	var form = {
	      	username: API_USER,
	      	nonce: nonce
	      };

	var formData = querystring.stringify(form);
	var contentLength = formData.length;

	var headers = {
		"X-API-KEY": API_KEY,
		"X-API-SIGN": signature,
		"X-API-NONCE": nonce,
		"Content-Length" : contentLength,
		"Content-Type": "application/x-www-form-urlencoded"
	}

	console.log("=============", headers, formData);
	return false;
	request({
	      url: full_url,
	      method: "POST",
	      headers: headers,
	      body:formData
		}, 
		function (error, response, body) {
		    if(!error){
		    	body = JSON.parse(body);
		    	if(response.statusCode == 200){
		    		console.log(body);
		    		resolve(body);
		    	}else{
		    		reject(error);
		    	}
		    }else{
		      console.log('error:',error);
		      	reject(error);
		    }
	    }
	);
  });
}

function getTransactions(body) {
  return new Promise(function(resolve, reject) 
  {

	var command_url = '/v1/transaction/getList3';
	var full_url = API_URL + command_url;
	var nonce = getNonce();

	var data = 'username=' + convertUsername(API_USER) + 
			   '&dateFrom=' + body.dateFrom +
			   '&dateTill=' + body.dateTill +
			   '&currency=' + body.currency +
			   '&page=' + body.page +
			   '&nonce='+ nonce;

	var form = {
	      	username: API_USER,
	      	dateFrom: body.dateFrom,
	      	dateTill: body.dateTill,
	      	currency: body.currency,
	      	page: body.page,
	      	nonce: nonce
	      };

	var formData = querystring.stringify(form);
	var contentLength = formData.length;

	const signature = makeSignature(nonce,data,command_url);
	var headers = {
		"X-API-KEY": API_KEY,
		"X-API-SIGN": signature,
		"X-API-NONCE": nonce,
		"Content-Length" : contentLength,
		"Content-Type": "application/x-www-form-urlencoded"
	}

	request({
	      url: full_url,
	      method: "POST",
	      headers: headers,
	      body:formData
		}, 
		function (error, response, body) {
		    if(!error){
		    	body = JSON.parse(body);
		    	if(response.statusCode == 200)
		    	{
		    		resolve(body);
		    	}
		    	else
		    	{
		    		reject(body);
		    	}
		    }else{
		      console.log('error:',error);
		      reject(error);
		    }
	    }
	);
  });
}

exports.sendMoney = function(body) {
  return new Promise(function(resolve, reject) 
  {
  	var command_url = '/v1/transaction/sendMoney';
	var full_url = API_URL + command_url;
	var nonce = getNonce();

	var data = 'username=' + convertUsername(API_USER) + 
			   '&amount='+ body.amount +
			   '&currency='+ body.currency +
			   '&recipient='+ body.recipient.replace(' ','_') +
			   '&account='+ body.to_account +
			   '&details='+ body.details +
			   '&nonce='+ nonce;

	var form = {
	      	username: API_USER,
	      	amount: body.amount,
	      	currency: body.currency,
	      	recipient: body.recipient.replace(' ','_'),
	      	account: body.to_account,
	      	details: body.details,
	      	nonce: nonce
	      };

	var formData = querystring.stringify(form);
	var contentLength = formData.length;

	const signature = makeSignature(nonce,data,command_url);

	var headers = {
		"X-API-KEY": API_KEY,
		"X-API-SIGN": signature,
		"X-API-NONCE": nonce,
		"Content-Length" : contentLength,
		"Content-Type": "application/x-www-form-urlencoded"
	}
	request({
	      url: full_url,
	      method: "POST",
	      headers: headers,
	      body:formData
		}, 
		function (error, response, resBody) {
		    if(!error)
		    {
		    	resBody = JSON.parse(resBody);
		    	if(response.statusCode == 200){
		    		console.log("Send Money response",resBody);

					resolve(resBody);
		    	}else{
			        reject(resBody);
			    }
		    }
		    else
		    {
		      console.log('error:',error);
		      reject(error);
		    }
	    }
	);
  });
}

function getNonce() //Get timestamp as nonce
{
	return new Date().getTime() + '' + parseInt(us.now()/100000000);
}

function convertUsername(username)
{
	return username.replace("@", "%40");
}

function makeSignature(nonce, data, command_url)
{
	const hashstring = nonce + data;
	const hashed = CryptoJS.SHA256(hashstring).toString(CryptoJS.enc.Latin1);
 	const encoded = CryptoJS.enc.Latin1.parse(command_url.concat(hashed));

 	return CryptoJS.HmacSHA512(encoded, API_SECRET).toString(CryptoJS.enc.Base64);
}

getBalance().then(function(e) {
	console.log(e);
});
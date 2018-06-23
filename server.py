import hashlib, time, hmac, base64, requests, json, datetime, subprocess, shlex
from os import environ as env
from dotenv import load_dotenv, find_dotenv

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

def getNonce():
	then = datetime.datetime.now()
	epochStr = (time.mktime(then.timetuple())*1e3 + then.microsecond/1e3) * 10000
	return str(int(epochStr))

def convertUsername(username):
	return username.replace("@", "%40")

def getBody(nonce):
	body = 'username=' + convertUsername(env.get("API_USER")) + '&nonce=' + nonce
	return body

def makeSignature(nonce, data, commandUrl):
	hashstring = nonce + data;
	hashed = hashlib.sha256(hashstring.encode('utf-8')).digest().decode("utf-8", "replace")
	encoded = commandUrl + hashed
	signature = base64.b64encode(hmac.new(env.get("API_SECRET").encode('utf-8'), encoded.encode('utf-8'), hashlib.sha512).digest())
	return signature.decode("utf-8")

def getHeaders(nonce, commandUrl):
	data = 'username=' + convertUsername(env.get("API_USER")) + '&nonce=' + nonce
	# signature = makeSignature(nonce, data, commandUrl)

	args = shlex.split('node makeSignature.js ' + env.get("API_SECRET") + ' ' + nonce + ' ' + data + ' ' + commandUrl)
	result = subprocess.run(args, stdout=subprocess.PIPE)
	signature = result.stdout.decode('utf-8').replace('\n', '')

	return {
		'X-API-KEY': env.get("API_KEY"),
		'X-API-SIGN': signature,
		'X-API-NONCE': nonce,
		'Content-Type': 'application/x-www-form-urlencoded'
	}

def getFullUrl(commandUrl):
	return env.get("API_URL") + commandUrl

def getBalance():
	nonce = getNonce()
	commandUrl = env.get("API_GETBALANCE")
	
	headers = getHeaders(nonce, commandUrl)
	body = getBody(nonce)

	r = requests.post(getFullUrl(commandUrl), headers = headers, data = body)
	print(json.loads(r.text))

getBalance()
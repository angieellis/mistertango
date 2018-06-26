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

def makeSignature(nonce, data, commandUrl):
	encoded = (nonce + data).encode()
	message = commandUrl.encode() + hashlib.sha256(encoded).digest()

	signature = hmac.new(
		env.get("API_SECRET").encode(),
		message,
		hashlib.sha512
	)
	sigdigest = base64.b64encode(signature.digest())

	return sigdigest.decode()

def getHeaders(nonce, commandUrl):
	data = 'username=' + convertUsername(env.get("API_USER")) + '&nonce=' + nonce
	signature = makeSignature(nonce, data, commandUrl)

	# args = shlex.split('node makeSignature.js ' + env.get("API_SECRET") + ' ' + nonce + ' ' + data + ' ' + commandUrl)
	# result = subprocess.run(args, stdout=subprocess.PIPE)
	# signature = result.stdout.decode('utf-8').replace('\n', '')

	return {
		'X-API-KEY': env.get("API_KEY"),
		'X-API-SIGN': signature,
		'X-API-NONCE': nonce,
		'Content-Type': 'application/x-www-form-urlencoded'
	}

def getFullUrl(commandUrl):
	return env.get("API_URL") + commandUrl

# /v1/transaction/getBalance
def getBalance():
	nonce = getNonce()
	commandUrl = "/v1/transaction/getBalance"
	
	headers = getHeaders(nonce, commandUrl)
	data = 'username=' + convertUsername(env.get("API_USER")) + '&nonce=' + nonce

	r = requests.post(getFullUrl(commandUrl), headers = headers, data = data)
	print(json.loads(r.text))

# /v1/user
def getGetList3(body):
	nonce = getNonce()
	commandUrl = "/v1/user"
	
	headers = getHeaders(nonce, commandUrl)
	data = (
		'username=' + convertUsername(env.get("API_USER")) +
		'&dateFrom=' + body["dateFrom"] +
		'&dateTill=' + body["dateTill"] +
		'&currency=' + body["currency"] +
		'&page=' + body["page"] +
		'&nonce=' + nonce
	)

	r = requests.post(getFullUrl(commandUrl), headers = headers, data = data)
	print(json.loads(r.text))

# /v1/user/phoneVerification
def phoneVerification(body):
	nonce = getNonce()
	commandUrl = "/v1/user/phoneVerification"

	headers = getHeaders(nonce, commandUrl)
	data = (
		'username=' + convertUsername(env.get("API_USER")) +
		'&phoneNumber=' + body["phoneNumber"] +
		'&action=' + body["action"] +
		'&code=' + body["code"] +
		'&nonce=' + nonce
	)

	r = requests.post(getFullUrl(commandUrl), headers = headers, data = data)
	print(json.loads(r.text))

# /v1/transaction/sendMoney
def sendMoney(body):
	nonce = getNonce()
	commandUrl = "/v1/transaction/sendMoney"

	headers = getHeaders(nonce, commandUrl)
	data = (
		'username=' + convertUsername(env.get("API_USER")) +
		'&amount=' + body["amount"] +
		'&currency=' + body["currency"] +
		'&recipient=' + body["recipient"] +
		'&account=' + body["account"] +
		'&details=' + body["details"]
	)

	r = requests.post(getFullUrl(commandUrl), headers = headers, data = data)
	print(json.loads(r.text))

# /v1/transaction/requestMoney
def requestMoney(body):
	nonce = getNonce()
	commandUrl = "/v1/transaction/requestMoney"

	headers = getHeaders(nonce, commandUrl)
	data = (
		'username=' + convertUsername(env.get("API_USER")) +
		'&amount=' + body["amount"] +
		'&currency=' + body["currency"] +
		'&from=' + body["from"] +
		'&details=' + body["details"]
	)

	r = requests.post(getFullUrl(commandUrl), headers = headers, data = data)
	print(json.loads(r.text))

# /v1/user/getSessionData
def getSessionData():
	nonce = getNonce()
	commandUrl = "/v1/user/getSessionData"

	headers = getHeaders(nonce, commandUrl)
	data = (
		'username=' + convertUsername(env.get("API_USER")) +
		'&nonce=' + nonce
	)

	r = requests.post(getFullUrl(commandUrl), headers = headers, data = data)
	print(json.loads(r.text))

getBalance()

while False:
	# Calling Functions

	# 1. 
	# getBalance()
	# 2. 
	# getGetList3(
	# 	{
	# 		'dateFrom': None,
	# 		'dateTill': None,
	# 		'currency': None,
	# 		'page': '1'
	# 	}
	# )
	# 3.
	# phoneVerification(
	# 	{
	# 		'phoneNumber': '+15162748174',
	# 		'action': 'get_code',
	# 		'code': 'check_code'
	# 	}
	# )
	# 4.
	# sendMoney(
	# 	{
	# 		'amount': '100',
	# 		'currency': 'EUR',
	# 		'recipient': '',
	# 		'account': '',
	# 		'details': ''
	# 	}
	# )
	# 5.
	# requestMoney(
	# 	{
	# 		'amount': '100',
	# 		'currency': 'EUR',
	# 		'from': '',
	# 		'details': ''
	# 	}
	# )
	# 6.
	getSessionData()
	time.sleep(int(env.get("TIME_DELAY"))) # Delay by seconds
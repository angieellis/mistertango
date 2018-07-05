import hashlib, time, hmac, base64, requests, json, datetime, urllib
from os import environ as env
from dotenv import load_dotenv, find_dotenv

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

last_updated_time = 0

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

def getHeaders(nonce, commandUrl, data):
	signature = makeSignature(nonce, data, commandUrl)

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
	
	data = {
		"username": env.get("API_USER"),
		"nonce": nonce
	}
	data = urllib.parse.urlencode(data)

	headers = getHeaders(nonce, commandUrl, data)
	r = requests.post(getFullUrl(commandUrl), headers = headers, data = data)
	status = json.loads(r.text)["status"]
	return status

# /v1/transaction/getList
def getGetList(body):
	nonce = getNonce()
	commandUrl = "/v1/transaction/getList"

	data = {
		"username": env.get("API_USER"),
		'nonce': nonce,
		"currency": body["currency"],
		"page": body["page"]
	}
	data = urllib.parse.urlencode(data)

	headers = getHeaders(nonce, commandUrl, data)
	r = requests.post(getFullUrl(commandUrl), headers = headers, data = data)
	print(json.loads(r.text))

# /v1/transaction/getList3
def getGetList3(body):
	nonce = getNonce()
	commandUrl = "/v1/transaction/getList3"
	
	data = {
		"username": env.get("API_USER"),
		"nonce": nonce,
		"currency": body["currency"],
		"page": body["page"]
	}
	data = urllib.parse.urlencode(data)

	headers = getHeaders(nonce, commandUrl, data)
	r = requests.post(getFullUrl(commandUrl), headers = headers, data = data)
	return json.loads(r.text)

# /v1/user/phoneVerification
def phoneVerification(body):
	nonce = getNonce()
	commandUrl = "/v1/user/phoneVerification"

	data = {
		"username": env.get("API_USER"),
		"phoneNumber": body["phoneNumber"],
		"action": body["action"],
		"code": body["code"],
		"nonce": nonce
	}
	data = urllib.parse.urlencode(data)

	headers = getHeaders(nonce, commandUrl, data)
	r = requests.post(getFullUrl(commandUrl), headers = headers, data = data)
	print(json.loads(r.text))

# /v1/transaction/sendMoney
def sendMoney(body):
	nonce = getNonce()
	commandUrl = "/v1/transaction/sendMoney"

	data = {
		"username": env.get("API_USER"),
		"amount": body["amount"],
		"currency": body["currency"],
		"recipient": body["recipient"],
		"account": body["account"],
		"details": body["details"]
	}
	data = urllib.parse.urlencode(data)

	headers = getHeaders(nonce, commandUrl, data)
	r = requests.post(getFullUrl(commandUrl), headers = headers, data = data)
	print(json.loads(r.text))

# /v1/transaction/requestMoney
def requestMoney(body):
	nonce = getNonce()
	commandUrl = "/v1/transaction/requestMoney"

	data = {
		"username": env.get("API_USER"),
		"amount": body["amount"],
		"currency": body["currency"],
		"from": body["from"],
		"details": body["details"]
	}
	data = urllib.parse.urlencode(data)

	headers = getHeaders(nonce, commandUrl, data)
	r = requests.post(getFullUrl(commandUrl), headers = headers, data = data)
	print(json.loads(r.text))

# /v1/user/getSessionData
def getSessionData():
	nonce = getNonce()
	commandUrl = "/v1/user/getSessionData"

	data = {
		"username": env.get("API_USER"),
		"nonce": nonce
	}
	data = urllib.parse.urlencode(data)

	headers = getHeaders(nonce, commandUrl, data)
	r = requests.post(getFullUrl(commandUrl), headers = headers, data = data)
	print(json.loads(r.text))

def updateGo(IBAN, amount, date):
	payload = {
		"IBAN": IBAN,
		"Amount": amount,
		"Date": date
	}

	print("===", payload)
	r = requests.post(env.get("GO_API_URL") + "/api/admin/user/balance", payload)
	print(json.loads(r.text))

def getEpochTime(date):
	utc_time = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S+%f")
	epoch_time = (utc_time - datetime.datetime(1970, 1, 1)).total_seconds()
	return epoch_time

while True:
	res = getGetList3({
		'dateFrom': '1530448312288961',
		'currency': 'EUR',
		'page': 1
	})

	try:
		last_list_time = getEpochTime(res["data"]["list"][0]["date"])
		if last_updated_time < last_list_time:
			last_updated_time = last_list_time
			for paylist in res["data"]["list"]:
				updateGo(paylist["other_side_account"], paylist["amount"], paylist["date"])
		print("Update GO service data successfully!")
	except:
		print("Something wrong in Mr.Tango api response")

	time.sleep(int(env.get("TIME_DELAY"))) # Delay by seconds
import credentials
 # Download the library from twilio.com/docs/libraries
from twilio.rest import TwilioRestClient
from flask import Flask, request, redirect
import twilio.twiml 
# Get these credentials from http://twilio.com/user/account

account_sid = credentials.sid
auth_token = credentials.authToken
client = TwilioRestClient(account_sid, auth_token)
app = Flask(__name__)

called = False
 
to_="+16508621107"
from_= "+16506035470"
url_="http://705be79e.ngrok.io/"
@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
	if called == False:
		call(to_, from_, url_)
		called = True
	resp = twilio.twiml.Response()
	with resp.gather(action="/handle-key") as inp:
		inp.say("Please enter a number and end with #")
	return str(resp)
 
@app.route("/handle-key", methods=['GET', 'POST'])
def handle_key():
	digit_pressed = request.values.get('Digits', None)
	resp = twilio.twiml.Response()
	resp.say("You entered " + digit_pressed)
	for i in range (1,int(digit_pressed)+1):
		if i%3 == 0:
			if i%5 == 0:
				resp.say("fizzbuzz")
			else:
				resp.say("fizz ")
		else:
			if i%5==0:
				resp.say("buzz ")
			else:
				resp.say(str(i))
	return str(resp)


if __name__ == "__main__":
    app.run(debug=True)

def call(call_to, call_from, call_url):
# Make the call
	call = client.calls.create(call_to, call_from, call_url)
	for c in client.calls.list():
		print ("From: " + c.from_formatted + " To: " + c.to_formatted)
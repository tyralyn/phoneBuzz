from flask import Flask, request, redirect, render_template, url_for
from twilio.rest import TwilioRestClient
import twilio.twiml 
import credentials
import sched
import uuid
import time
import callEntry
#import helperFunctions
import collections

#taken from credentials.py file: sid and authtoken required to make calls
account_sid = credentials.sid
auth_token = credentials.authToken
account_phone = credentials.callFrom
request_url = credentials.requestURL
client = TwilioRestClient(account_sid, auth_token)


app = Flask(__name__)

s=sched.scheduler(time.time, time.sleep) #for delays
li = collections.OrderedDict() #storage system for app


#helper function: determines whether the last call the user tried to make was invalid or not
def lastCallInvalid():
	try:
		lastKeyInDict= next(reversed(li))
		return (li[lastKeyInDict].validNumberFlag)
	except (StopIteration):
		return True

def handle_call(replayingCall = None):
	callId = str(uuid.uuid4())
	if replayingCall==None:
		num = request.form['number']
		delay = request.form['delay']
		li[callId]=(callEntry.callEntry(num, delay, replayingCall))
	else:
		num=li[replayingCall].num
		delay=li[replayingCall].delay
		li[callId]=(callEntry.callEntry(num, delay, replayingCall))
		li[callId].setFizzBuzz(li[replayingCall].fizzBuzz)
	s.enter(li[callId].delay, 1, make_call, (1, callId))
	s.run()

def make_call(i, callId):
	to_ = li[callId].num
	from_ = account_phone
	get_input_url_ = request_url+"get-input/"+callId
	replay_url_=request_url+"replay-call/"+callId
	try:
		if li[callId].replay==None:
			call = client.calls.create(to_,  from_, get_input_url_)
		else:
			call = client.calls.create(to_,  from_, replay_url_)
	except (twilio.rest.exceptions.TwilioRestException):
		li[callId].validNumberFlag = False

#takes in response item and performs fizzbuzz to listener
def fizzBuzz(callId, resp):
	n = li[callId].fizzBuzz
	resp.say("You entered " + n+". ")
	for i in range (1,int(n)+1):
		if i%3 == 0:
			if i%5 == 0:
				resp.say("fizzbuzz,")
			else:
				resp.say("fizz, ")
		else:
			if i%5==0:
				resp.say("buzz, ")
			else:
				resp.say(str(i))
	resp.say("fizzbuzz is complete.")


#entry point for application, renders /templates/index.html for input box
@app.route('/')
def start_here(): 
	return render_template('index.html', l=li, lastCallInvalid = lastCallInvalid())

#performs actions if replay button is pressed
@app.route("/get-phonecall", methods=['GET', 'POST'])
def get_phonecall():
	callId=request.form['callId']
	handle_call(callId)
	return redirect('/')

#performs actions if a new call (non-replay) is initiated
@app.route("/get-phone-number-and-delay", methods=['GET', 'POST']) 
def get_phone_number_and_call():
	handle_call()
	return redirect(('/'))

#recieves call made by call function for non-replay calls, prompts user for input
@app.route("/get-input/<callId>", methods=['GET', 'POST'])
def get_input(callId):
	resp = twilio.twiml.Response()
	with resp.gather(action="/handle-key/"+str(callId)) as inp:
		inp.say("Please enter a number and end with #")
	return str(resp)

#handles user input for non-replay calls
@app.route("/handle-key/<callId>", methods=['GET', 'POST'])
def handle_key(callId):
	resp = twilio.twiml.Response()
	digit_pressed = request.values.get('Digits', str(0))
	li[callId].fizzBuzz=digit_pressed
	fizzBuzz(callId, resp)
	return str(resp)

#handles replay calls
@app.route("/replay-call/<callId>", methods=['GET', 'POST'])
def replay_call(callId):
	resp = twilio.twiml.Response()
	fizzBuzz(callId, resp)
	return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
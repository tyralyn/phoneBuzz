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
client = TwilioRestClient(account_sid, auth_token)

app = Flask(__name__)

s=sched.scheduler(time.time, time.sleep)
i = False
li = collections.OrderedDict()

#entry point for application, renders /templates/index.html for input box
@app.route('/')
def start_here(): 
	return render_template('index.html', l=li, lastCallInvalid = lastCallInvalid())

def lastCallInvalid():
	try:
		lastKeyInDict= next(reversed(li))
		return (li[lastKeyInDict].validNumberFlag)
	except (StopIteration):
		return True


#obtains input (phone number) from input box, redirects to function that makes call
@app.route("/get-phone-number-and-delay", methods=['GET', 'POST']) 
def get_phone_number_and_call():
	handle_call()
	print(i," gnac")
	return redirect(('/'))
	#return render_template('index.html', l=li, invalidPhone = i)

def handle_call():
	global i
	i = False
	num = request.form['number']
	delay = request.form['delay']
	callId = str(uuid.uuid4())
	li[callId]=(callEntry.callEntry(num, delay))
	s.enter(li[callId].delay, 1, make_call, (li[callId].num, "+16506035470", "http://8b4cd4ed.ngrok.io/"+"get-input/"+callId, callId))
	s.run()

def make_call(to_, from_, url_, callId):
	try:
		call = client.calls.create(to_,  from_, url_)
	except (twilio.rest.exceptions.TwilioRestException):
		li[callId].validNumberFlag = False
		print(i," make call")
		#return render_template('index.html', l=li, invalidPhone = i)
	#finally: 	
		#print(i)

#recieves call made by call function, prompts user for input
#@app.route("/get-input", methods=['GET', 'POST'])
@app.route("/get-input/<callId>", methods=['GET', 'POST'])
def get_input(callId):
	resp = twilio.twiml.Response()
	with resp.gather(action="/handle-key/"+str(callId)) as inp:
		inp.say("Please enter a number and end with #")
	return str(resp)

#takes input from user and goes through fizzbuzz process
@app.route("/handle-key/<callId>", methods=['GET', 'POST'])
def handle_key(callId):
	digit_pressed = request.values.get('Digits', str(0))
	resp = twilio.twiml.Response()
	resp.say("You entered " + digit_pressed+". ")
	for i in range (1,int(digit_pressed)+1):
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
	li[callId].fizzBuzz=digit_pressed
	print(li[callId].fizzBuzz)
	return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
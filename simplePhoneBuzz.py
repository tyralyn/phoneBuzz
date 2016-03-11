from flask import Flask, request, redirect, render_template
from twilio.rest import TwilioRestClient
import twilio.twiml 
import credentials
import sched
import time
import callEntry
import helperFunctions


account_sid = credentials.sid
auth_token = credentials.authToken
client = TwilioRestClient(account_sid, auth_token)
app = Flask(__name__)
s=sched.scheduler(time.time, time.sleep)

li = [callEntry.callEntry("sample")]


#entry point for application, renders /templates/index.html for input box
@app.route('/')
def start_here(): 
	return render_template('index.html', l=li)

#obtains input (phone number) from input box, redirects to function that makes call
@app.route("/get-phone-number-and-delay", methods=['GET', 'POST']) 
def get_phone_number_and_call():
	#get phone number from html input, parse out digits, make int a phone number
	phone_num = request.form['number']
	num=helperFunctions.handlePhoneNumber(phone_num)

	#get delay from html input. if invalid input, choose default delay of zero
	delay = request.form['delay']
	delayVal = 0 if not helperFunctions.isInt(delay) else int(delay)


	resp = twilio.twiml.Response()

	li.append(callEntry.callEntry(num))
	make_call(num, "+16506035470", "http://8b4cd4ed.ngrok.io/"+"get-input")
	
	#s.enter(delayVal,1,make_call, (phoneNum, "+16506035470", "http://705be79e.ngrok.io/"+"get-input"))
	#s.run()
	return render_template('index.html', l=li)

def make_call(to_, from_, url_):
		call = client.calls.create(to_,  from_, url_)

#recieves call made by call function, prompts user for input
@app.route("/get-input", methods=['GET', 'POST'])
def get_input():
	resp = twilio.twiml.Response()
	with resp.gather(action="/handle-key") as inp:
		inp.say("Please enter a number and end with #")
	return str(resp)

#takes input from user and goes through fizzbuzz process
@app.route("/handle-key", methods=['GET', 'POST'])
def handle_key():
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
	return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
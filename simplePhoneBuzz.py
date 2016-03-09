from flask import Flask, request, redirect, render_template
from twilio.rest import TwilioRestClient
import twilio.twiml # Download the library from twilio.com/docs/libraries
#import dialingPhoneBuzz
import credentials
import re
 

account_sid = credentials.sid
auth_token = credentials.authToken
client = TwilioRestClient(account_sid, auth_token)
app = Flask(__name__)

#entry point for application, renders /templates/index.html for input box
@app.route('/')
def start_here():
	return render_template('index.html')

#obtains input (phone number) from input box, redirects to function that makes call
@app.route("/get-phone-number", methods=['GET', 'POST']) 
def get_phone_number_and_call():
	phone_num = request.form['number']
	digits=re.findall(r'\d+', phone_num)
	phoneNum="+"+"".join(map(str,digits))
	resp = twilio.twiml.Response()
	call = client.calls.create(to=phoneNum,  from_= "+16506035470", url="http://705be79e.ngrok.io/"+"get-input")
	return str(resp)

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
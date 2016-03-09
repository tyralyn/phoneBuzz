from flask import Flask, request, redirect, render_template
from twilio.rest import TwilioRestClient
import twilio.twiml # Download the library from twilio.com/docs/libraries
#import dialingPhoneBuzz
import credentials
 

account_sid = credentials.sid
auth_token = credentials.authToken
client = TwilioRestClient(account_sid, auth_token) 
 
app = Flask(__name__)


@app.route('/')
def hello_world():
	return render_template('index.html')

@app.route("/get_phone_number", methods=['GET', 'POST']) 
def get_phone_number():
	phone_num = request.form['number']
	print('phone number is '+phone_num)
	return redirect('/make_call')

@app.route("/make_call", methods=['GET', 'POST'])
def call():
	call = client.calls.create(to="+16508621107",  from_= "+16506035470", url="http://705be79e.ngrok.io/")

	for c in client.calls.list():
		print ("From: " + c.from_formatted + " To: " + c.to_formatted)
	return redirect('/respond_to_call')

@app.route("/respond_to_call", methods=['GET', 'POST'])
def respond_to_call():
    """Respond to incoming requests."""
    print("A")
    resp = twilio.twiml.Response()
    print("B")
    with resp.gather(action="/handle-key") as inp:
    	resp.say("Please enter a number and end with #")
    	print("C")
    print("D")
    digit_pressed = request.values.get('Digits', None)
    print("E")
    resp.say("You entered " + digit_pressed)
    print("F")
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
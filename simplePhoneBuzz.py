from flask import Flask, request, redirect
import twilio.twiml
 
app = Flask(__name__)
 
@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    """Respond to incoming requests."""
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
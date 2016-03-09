import credentials
 # Download the library from twilio.com/docs/libraries
from twilio.rest import TwilioRestClient
 
# Get these credentials from http://twilio.com/user/account
account_sid = credentials.sid
auth_token = credentials.authToken
client = TwilioRestClient(account_sid, auth_token)
 


# Make the call
def call():
	call = client.calls.create(to="+16508621107",  from_= "+16506035470", url="http://705be79e.ngrok.io/")

	for c in client.calls.list():
		print ("From: " + c.from_formatted + " To: " + c.to_formatted)

call()
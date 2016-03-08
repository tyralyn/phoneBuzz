import credentials
 # Download the library from twilio.com/docs/libraries
from twilio.rest import TwilioRestClient
 
# Get these credentials from http://twilio.com/user/account
account_sid = credentials.sid
auth_token = credentials.authToken
client = TwilioRestClient(account_sid, auth_token)
 


# Make the call
call = client.calls.create(to="+16508621107",  # Any phone number
                           from_= "+16506035470", # Must be a valid Twilio number
                           url="http://705be79e.ngrok.io/")
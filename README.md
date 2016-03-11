INTRODUCTION

This is Tyralyn Tran's entry for Lendup's PhoneBuzz coding challenge. 

--------------------------------------------------------------------

BUILD/RUN INFO

* instructions provided are for a Windows 7 machine running Python 3.5.1. Adapted from here: https://www.twilio.com/docs/quickstart/python/devenvironment
* requires virtualenv and pip to be preinstalled

1. Set up virtual environment

	virtualenv --no-site-packages .

2. Activate virtual environment

	Scripts\activate.bat

3. Install packages listed in req.txt

	pip install -r req.txt

4. To run, call the simplePhoneBuzz file

	python simplePhoneBuzz.py

In order to sub in different Twilio account credentials, open up crendentials.py. The from number is set to Twilio's approved test number. Edit the variables accordingly in the following manner: 

sid="aaaaaaaaaaaa"
authToken="bbbbbbbbbbb"

callFrom="+15005550006"
requestURL="http://8b4cd4ed.ngrok.io/"

--------------------------------------------------------------------

SERVER/HOSTING INFO

Currently, the site is hosted on an ngrok tunnel to my personal machine. It is currently located at http://8b4cd4ed.ngrok.io/. 
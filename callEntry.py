from datetime import datetime
import re

#helper function to determine whether string is an integer
def isInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

class callEntry:
	def __init__(self, num, delay, replay = None):
		#time
		self.date = datetime.now().date()
		self.time = datetime.now().time()
		#delay
		self.delay = "" if delay == None else self.handleDelayValue(delay)
		#number
		self.rawNumString = num
		self.num=self.handlePhoneNumber(num)
		#fizzbuzz value
		self.fizzBuzz= "none"
		#validPhoneFlag
		self.validNumberFlag=True
		#is this a replay of a previous call?
		self.replay = replay

	def setNumber(self, s):
		self.number = s

	def setDelay(self, s):
		self.delay = s

	def setFizzBuzz(self, s):
		self.fizzBuzz=s

	def handlePhoneNumber(self, s):
		digits=re.findall(r'\d+', s)
		digitsString="".join(map(str,digits))
		if len(digitsString) == 10:
			return ("+1"+digitsString)
		elif len(digitsString)==11:
			return ("+"+digitsString)
		else:
			return (digitsString)

	#helper function to determine whether delay value is valid: only takes integers
	def handleDelayValue(self, s):
		return (0 if not isInt(s) else int(s))
		
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
	def __init__(self, num, delay=None):
		#time
		self.now = datetime.now()
		#delay
		self.delay = "" if delay == None else self.handleDelayValue(delay)
		#number
		self.rawNumString = num
		self.num=self.handlePhoneNumber(num)
		#fizzbuzz value
		self.fizzBuzz= ""

	def setNumber(s):
		self.number = s

	def setDelay(s):
		self.delay = s

	def setFizzBuzz(s):
		self.fizzBuzz=s

	def printCallEntry(self):
		return ('{:%Y-%m-%d %H:%M:%S}'.format(self.now)+" "+str(num))

	def handlePhoneNumber(self, s):
		digits=re.findall(r'\d+', s)
		digitsString="".join(map(str,digits))
		if len(digitsString) == 10:
			return ("+1"+digitsString)
		elif len(digitsString)==11:
			return ("+"+digitsString)
		else:
			return ("invalid number: "+s)

#helper function to determine whether delay value is valid
	def handleDelayValue(self, s):
		return (0 if not isInt(s) else int(s))
		
from datetime import datetime

class callEntry:
	def __init__(self, num):
		#time
		self.now = datetime.now()
		#delay
		self.delay = ""
		#number
		self.number = num
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
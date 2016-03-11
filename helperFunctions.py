import re

#helper function to determine whether string is an integer
def isInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

#helper function to determine whether phone number is valid
#takes american numbers only
def handlePhoneNumber(s):
	digits=re.findall(r'\d+', s)
	digitsString="".join(map(str,digits))
	if len(digitsString) == 10:
		return ("+1"+digitsString)
	elif len(digitsString)==11:
		return ("+"+digitsString)
	else:
		return -1

#helper function to determine whether delay value is valid
def handleDelayValue(s):
	return (0 if not isInt(s) else int(s))
		



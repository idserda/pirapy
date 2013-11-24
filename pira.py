import serial, time

class PiraRDS(object):

	SUCCES = "+"
	UNKNOWN_COMMAND = "!"
	INVALID_ARGUMENT = "-"
	PROCESSED_PARTIALLY = "/"

	__EOF = chr(13) + chr(10) + chr(13) + chr(10)

	def __init__(self, port, baudrate=2400, autostore=False):
		self.serial = serial.Serial(port=port, baudrate=baudrate, bytesize=serial.EIGHTBITS, 
					     parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
					     timeout = 10)
		self.autostore = autostore

		for func in  {"PI", "ECHO", "DPS1", "DPS1ENQ", "DPS2", "PS", "PTYN", "RT1", "RT2", "TPS"}:
			self.__createAccessMethod(func)

		self.setEcho(0)

	# Getter/setter methods

	def setPi(self, pi):
		pi = pi.upper()
		numeric = int(pi, 16)
		if numeric > 65535 or numeric < 4096:
			raise ValueError("PI must be between 1000 and FFFF")

		return self.__setValue("PI", pi.strip())

	def isRt1en(self):
		return True if self.__getValue("RT1EN") == "1" else False;

	def setRt1en(self, value):
		return self.__setValue("RT1EN", 1 if value else 0)

	def isRt2en(self):
		return True if self.__getValue("RT2EN") == "1" else False;

	def setRt2en(self, value):
		return self.__setValue("RT2EN", 1 if value else 0)

	# Store 

	def store(self):
		return self.__executeCommand("*ALL")

	# Private methods

	def __getValue(self, attribute):
		value = self.__executeCommand(attribute)
		return value[0:-3]

	def __setValue(self, attribute, value):
		cmd = "%s=%s" % (attribute, value)
		cmdResult = self.__executeCommand(cmd)

		if cmdResult == PiraRDS.SUCCES and self.autostore:
			cmdResult = self.store()

		return cmdResult

	def __executeCommand(self, command):
		self.serial.write(command)
		self.serial.write(chr(13))
		return self.__read()

	def __read(self):
		ret = str()
		while True:
			ret = ret + self.serial.read()
			if ret[-4:] == PiraRDS.__EOF:
				return ret.strip()

	def __createAccessMethod(self, propertyName):
		def setAttribute(self, propertyValue):           
			return self.__setValue(propertyName, propertyValue)
		def getAttribute(self):
			return self.__getValue(propertyName)
		
		if not hasattr(self.__class__, 'set'+ propertyName.capitalize()):
			setattr(self.__class__, 'set'+ propertyName.capitalize(), setAttribute)
		if not hasattr(self.__class__, 'get'+ propertyName.capitalize()):
			setattr(self.__class__, 'get'+ propertyName.capitalize(), getAttribute)


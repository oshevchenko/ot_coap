from model import device

class model(device.model):
	def __init__(self, connection):
		self.connection = connection
		self.objName = 'DEVICE'
		self.devType = 'TempSensor'

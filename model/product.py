from model import default

class model(default.model):
	def __init__(self, connection):
		self.connection = connection
		self.objName = 'PRODUCT'

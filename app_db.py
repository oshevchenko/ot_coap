import sqlite3

from model import empty, menu, client, seller, device, product

class app_db:

	model={}

	def __init__(self, databaseName):
		self.connection = sqlite3.connect(databaseName, check_same_thread=False)
		print(self.connection)
		self.model_empty = empty.model()

		self.model['menu'] = menu.model()
		self.model['client'] = client.model(self.connection)
		self.model['seller'] = seller.model(self.connection)
		self.model['device'] = device.model(self.connection)
		self.model['product'] = product.model(self.connection)

	def __del__(self):
		self.connection.close()

	def getModel(self, modelName):
		if modelName in self.model:
			return self.model[modelName]
		else:
			return self.model_empty

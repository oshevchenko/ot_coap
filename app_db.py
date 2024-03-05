import sqlite3
import logging
from model import empty, menu, client, seller, device, product, device_temperature, device_emergency

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
		self.model['device_temperature'] = device_temperature.model(self.connection)
		self.model['device_emergency'] = device_emergency.model(self.connection)
		logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w",
							format="%(asctime)s %(levelname)s %(message)s")
		logging.debug("A DEBUG Message")
		logging.info("An INFO")
		logging.warning("A WARNING")
		logging.error("An ERROR")
		logging.critical("A message of CRITICAL severity")

	def __del__(self):
		self.connection.close()

	def getModel(self, modelName):
		if modelName in self.model:
			return self.model[modelName]
		else:
			return self.model_empty

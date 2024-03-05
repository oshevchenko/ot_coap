import sqlite3
import logging
from logging.handlers import RotatingFileHandler
import sys
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
		# log_name="coap.log"
		# log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')

		# handler = RotatingFileHandler(log_name, mode='a', maxBytes=5*1024*1024, 
		# 								backupCount=2, encoding=None, delay=0)
		# handler.setFormatter(log_formatter)
		# handler.setLevel(logging.INFO)
		# log = logging.getLogger()
		# log.addHandler(handler)

		# handler = logging.StreamHandler(sys.stdout)
		# handler.setFormatter(log_formatter)
		# handler.setLevel(logging.INFO)
		# log.addHandler(handler)

		# log.setLevel(logging.INFO)

	def __del__(self):
		self.connection.close()

	def getModel(self, modelName):
		if modelName in self.model:
			return self.model[modelName]
		else:
			return self.model_empty

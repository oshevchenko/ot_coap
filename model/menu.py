import os
import json
import codecs

class model:
	#def __init__(self, connection, objName):
		#self.connection = connection
		#self.objName = objName

	def create(self, data = None ):
		return {}

	def read(self, id = None ):
		file_json = 'menu.json'
		menu = {}
		if os.path.isfile(file_json):
			with codecs.open(file_json, 'r', 'utf-8') as file_data:
				menu = json.load(file_data)
				return menu
		return menu

	def update(self, id, data):
		return {}

	def delete(self, id):
		return {}

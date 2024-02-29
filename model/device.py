from model import default

class model(default.model):
	def __init__(self, connection):
		self.connection = connection
		self.objName = 'DEVICE'
		self.devType = None
	def update(self, id, data):
		result = {'result':'ERROR', 'errors':['Failed to update']}
		if id != 0:
			result = super().update(id, data)
		else:
			with self.connection:
				cursor = self.connection.cursor()
				cursor.execute("SELECT * FROM {0} WHERE(serial='{1}');".format(self.objName, data["serial"]))
				field_names = list(map(lambda x: x[0], cursor.description))
				rows = cursor.fetchall()
				print('rows {} self.objName {}'.format(rows, self.objName))
				if (len(rows) == 0):
					# Create new record
					print('create new record {} {}'.format(self.objName, data))
					result = super().create(data)
				else:
					record = {}
					for row in rows:
						field_i = 0
						for field in field_names:
							record[field] = row[field_i]
							field_i += 1
					result = super().update(record['id'], data)
		return result

	def read(self, id = None ):
		with self.connection:
			cursor = self.connection.cursor()
			if id == None:
				if self.devType == None:
					cursor.execute('SELECT * FROM {0};'.format(self.objName))
				else:
					cursor.execute("SELECT * FROM {0} WHERE(devtype='{1}');".format(self.objName, self.devType))
				field_names = list(map(lambda x: x[0], cursor.description))
				rows = cursor.fetchall()
				records = []
				for row in rows:
					field_i = 0
					record = {}
					for field in field_names:
						record[field] = row[field_i]
						field_i += 1
					records.append(record)
				return records
			else:
				cursor.execute('SELECT * FROM {0} WHERE(id={1});'.format(self.objName, id))
				field_names = list(map(lambda x: x[0], cursor.description))
				rows = cursor.fetchall()
				record = {}
				for row in rows:
					field_i = 0
					for field in field_names:
						record[field] = row[field_i]
						field_i += 1

				return record
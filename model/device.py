from model import default

class model(default.model):
	def __init__(self, connection):
		self.connection = connection
		self.objName = 'DEVICE'

	def update(self, data):
		result = {'result':'ERROR', 'errors':['Failed to update']}
		with self.connection:
			cursor = self.connection.cursor()
			cursor.execute('SELECT * FROM {0} WHERE(serial={1});'.format(self.objName, data["serial"]))
			field_names = list(map(lambda x: x[0], cursor.description))
			rows = cursor.fetchall()
			print(rows)
			if (len(rows) == 0):
				# Create new record
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
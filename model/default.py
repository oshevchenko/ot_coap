class model:
	def __init__(self, connection, objName):
		self.connection = connection
		self.objName = objName

	def create(self, data = None ):
		cursor = self.connection.cursor()
		fields_list = []
		values_list = []
		for field in data:
			fields_list.append(field)
			values_list.append('"{0}"'.format(data[field]))
		fields = ','.join(fields_list)
		values = ','.join(values_list)

		SQL = 'INSERT INTO {0} ({1}) VALUES({2})'.format(self.objName, fields, values)
		try:
			cursor.execute(SQL)
			self.connection.commit()
			result = {'result':'OK', 'id':cursor.lastrowid}
		except Exception:
			result = {'result':'ERROR', 'errors':['Failed to create']}
		finally:
			return result

	def read(self, id = None ):
		cursor = self.connection.cursor()
		if id == None:
			cursor.execute('SELECT * FROM {0};'.format(self.objName))
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

	def update(self, id, data):
		cursor = self.connection.cursor()
		fields_values_list = []
		for field in data:
			fields_values_list.append('{0}="{1}"'.format(field, data[field]))

		fields_values = ','.join(fields_values_list)
		SQL = 'UPDATE {0} SET {2} WHERE(id={1});'.format(self.objName, id, fields_values)
		try:
			cursor.execute(SQL)
			self.connection.commit()
			result = {'result':'OK'}
		except Exception:
			result = {'result':'ERROR', 'errors':['Failed to update']}
		finally:
			return result

	def delete(self, id):
		cursor = self.connection.cursor()
		try:
			cursor.execute('DELETE FROM {0} WHERE(id={1});'.format(self.objName, id))
			self.connection.commit()
			result = {'result':'OK'}
		except Exception:
			result = {'result':'ERROR', 'errors':['Failed to delete']}
		finally:
			return result


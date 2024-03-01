import asyncio

from aiocoap import *
from aiocoap import PUT
from aiocoap.message import Message

from model import default
import json

async def led_on(ipv6_addr, led_number):
	print('led_on {}'.format(led_number))
	context = await Context.create_client_context()

	await asyncio.sleep(2)
	# payload = b'{"id":4, "serial": "4444444444", "name": "Director clock", "ipv6": "fda1:98ec:3c8d:a291:167:99e1:b956:56ba",\
	#     "lastreport": "2024-02-23 11:10:15", "swver": "v0.0.3", "devtype": "dig. clock", "devrole": "router"}'

	payload = b'{"ctrltype": "led", "id": 2, "value": 1}'
	request = Message(code=PUT, payload=payload, uri="coap://[fd22:11f9:7dd5:1:5d30:ca15:60b0:21bc]/controldata")

	response = await context.request(request).response

	print('Result: %s\n%s'%(response.code, response.payload.decode('utf-8')))

async def led_off(ipv6_addr, led_number):
	print('led_off {}'.format(led_number))
	context = await Context.create_client_context()

	await asyncio.sleep(2)
	# payload = b'{"id":4, "serial": "4444444444", "name": "Director clock", "ipv6": "fda1:98ec:3c8d:a291:167:99e1:b956:56ba",\
	#     "lastreport": "2024-02-23 11:10:15", "swver": "v0.0.3", "devtype": "dig. clock", "devrole": "router"}'

	payload = b'{"ctrltype": "led", "id": 2, "value": 0}'
	request = Message(code=PUT, payload=payload, uri="coap://[fd22:11f9:7dd5:1:5d30:ca15:60b0:21bc]/controldata")

	response = await context.request(request).response

	print('Result: %s\n%s'%(response.code, response.payload.decode('utf-8')))

async def led_blink(ipv6_addr, led_number):
	"""Perform a single PUT request to localhost on the default port, URI
	"/other/block". The request is sent 2 seconds after initialization.

	The payload is bigger than 1kB, and thus sent as several blocks."""

	print('led_blink {}'.format(led_number))
	context = await Context.create_client_context()

	await asyncio.sleep(2)
	# payload = b'{"id":4, "serial": "4444444444", "name": "Director clock", "ipv6": "fda1:98ec:3c8d:a291:167:99e1:b956:56ba",\
	#     "lastreport": "2024-02-23 11:10:15", "swver": "v0.0.3", "devtype": "dig. clock", "devrole": "router"}'

	payload = b'{"ctrltype": "led", "id": 2, "value": 2}'
	request = Message(code=PUT, payload=payload, uri="coap://[fd22:11f9:7dd5:1:5d30:ca15:60b0:21bc]/controldata")

	response = await context.request(request).response

	print('Result: %s\n%s'%(response.code, response.payload.decode('utf-8')))

async def coap_send_led(ipv6_addr, led_list):
	"""Perform a single PUT request to localhost on the default port, URI
	"/other/block". The request is sent 2 seconds after initialization.
	The payload is bigger than 1kB, and thus sent as several blocks."""

	print('ipv6_addr {} led_list {}'.format(ipv6_addr, led_list))
	context = await Context.create_client_context()

	await asyncio.sleep(2)
	payload_dict = {}
	payload_dict['ctrltype'] = 'led'
	payload_dict['value'] = led_list
	payload = json.dumps(payload_dict).encode('utf-8')
	print('payload {} type {}'.format(payload, type(payload)))
	coap_uri = "coap://[{0}]/controldata".format(ipv6_addr)
	request = Message(code=PUT, payload=payload, uri=coap_uri)
	response = await context.request(request).response
	print('Result: %s\n%s'%(response.code, response.payload.decode('utf-8')))


class model(default.model):
	def __init__(self, connection):
		self.connection = connection
		self.objName = 'DEVICE'
		self.devType = None
	def update(self, id, data):
		result = {'result':'ERROR', 'errors':['Failed to update']}
		if id != 0:
			do_coap_send = False
			led_cmd = data.get('led_cmd', None)
			ipv6_addr = data.get('ipv6', None)
			if led_cmd != None and ipv6_addr != None:
				led_cmd_list_send = []
				led_cmd_list_processed = []
				led_cmd_list = led_cmd.split(',')
				for cmd in led_cmd_list:
					if cmd == 'on':
						led_cmd_list_send.append('on')
						led_cmd_list_processed.append("_on_")
						do_coap_send = True
					elif cmd == 'off':
						led_cmd_list_send.append('off')
						led_cmd_list_processed.append("_off_")
						do_coap_send = True
					elif cmd == 'bon':
						led_cmd_list_send.append('blink')
						led_cmd_list_processed.append("_bon_")
						do_coap_send = True
					elif cmd == 'boff':
						led_cmd_list_send.append('off')
						led_cmd_list_processed.append("_boff_")
						do_coap_send = True
					elif cmd in [ '_on_', '_off_', '_bon_', '_boff_']:
						led_cmd_list_send.append("x")
						led_cmd_list_processed.append(cmd)
					else:
						led_cmd_list_send.append("x")
						led_cmd_list_processed.append("x")
				data['led_cmd'] = ','.join(led_cmd_list_processed)
				print("data['led_cmd'] {}".format(data['led_cmd']))
			result = super().update(id, data)
			if do_coap_send:
				try:
					asyncio.run(coap_send_led(ipv6_addr, led_cmd_list_send))
				except Exception as e:
					print('Error: {}'.format(e))
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
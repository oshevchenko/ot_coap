import functools  # at the top with the other imports
import logging
import asyncio
import threading

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

	# print('Result: %s\n%s'%(response.code, response.payload.decode('utf-8')))
	logging.info('Result: %s\n%s'%(response.code, response.payload.decode('utf-8')))

async def coap_send_led(ipv6_addr, led_list):
	"""Perform a single PUT request to localhost on the default port, URI
	"/other/block". The request is sent 2 seconds after initialization.
	The payload is bigger than 1kB, and thus sent as several blocks."""

	# print('ipv6_addr {} led_list {}'.format(ipv6_addr, led_list))
	logging.info('ipv6_addr {} led_list {}'.format(ipv6_addr, led_list))
	context = await Context.create_client_context()

	# await asyncio.sleep(2)
	payload_dict = {}
	payload_dict['ctrltype'] = 'led'
	payload_dict['value'] = led_list
	payload = json.dumps(payload_dict).encode('utf-8')
	# print('payload {} type {}'.format(payload, type(payload)))
	logging.info('payload {} type {}'.format(payload, type(payload)))
	coap_uri = "coap://[{0}]/controldata".format(ipv6_addr)
	request = Message(code=PUT, payload=payload, uri=coap_uri)
	response = await context.request(request).response
	# print('Result: %s\n%s'%(response.code, response.payload.decode('utf-8')))
	logging.info('Result: %s\n%s'%(response.code, response.payload.decode('utf-8')))


class model(default.model):
	def __init__(self, connection):
		self.connection = connection
		self.objName = 'DEVICE'
		self.devType = None
	def update(self, id, data):
		result = {'result':'ERROR', 'errors':['Failed to update']}
		logging.info('update id {} data {}'.format(id, data))
		if id != 0:
			do_coap_send_led = False
			coap_action = data.get('coap_action', None)
			if coap_action == 'led_on':
				data['coap_action'] = 'done'
				led_cmd = data.get('led_on_cmd', None)
				led_cmd_list_send = []
				led_cmd = led_cmd.replace(" ", "")
				led_cmd_list = led_cmd.split(',')
				for cmd in led_cmd_list:
					if cmd in ['on', 'blink']:
						led_cmd_list_send.append(cmd)
						do_coap_send_led = True
					else:
						led_cmd_list_send.append("x")
				data['led_on_cmd'] = ','.join(led_cmd_list_send)
			elif coap_action == 'led_off':
				data['coap_action'] = 'done'
				led_cmd = data.get('led_off_cmd', None)
				led_cmd_list_send = []
				led_cmd = led_cmd.replace(" ", "")
				led_cmd_list = led_cmd.split(',')
				for cmd in led_cmd_list:
					if cmd == 'off':
						led_cmd_list_send.append(cmd)
						do_coap_send_led = True
					else:
						led_cmd_list_send.append("x")
				data['led_off_cmd'] = ','.join(led_cmd_list_send)
			else:
				led_cmd = None
			result = super().update(id, data)
			if do_coap_send_led:
				try:
					ipv6_addr = data.get('ipv6', None)
					logging.info("ipv6_addr: {}.".format(ipv6_addr))
					# loop = asyncio.get_event_loop()
					# logging.info("loop {} ipv6_addr: {}.".format(loop, ipv6_addr))

					# loop.run_in_executor(None, coap_send_led, p)
					_thread = threading.Thread(target=asyncio.run, args=(coap_send_led(ipv6_addr, led_cmd_list_send),))
					_thread.start()

					# loop.run_in_executor(None, functools.partial(coap_send_led, data={
					# 	'ipv6_addr': ipv6_addr,
					# 	'led_list': led_cmd_list_send
					# }))
					# asyncio.run(coap_send_led(ipv6_addr, led_cmd_list_send))
				except Exception as e:
					logging.error('Error: {}'.format(e))
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
		print('result {}'.format(result))
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
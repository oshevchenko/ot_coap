import functools  # at the top with the other imports
import logging
import asyncio
import threading

from aiocoap import *
from aiocoap import PUT
from aiocoap.message import Message
from model.coap_client import coap_client

from model import default
import json

class model(default.model):
	def __init__(self, connection):
		self.connection = connection
		self.objName = 'DEVICE'
		self.devType = None
	def update(self, id, data):
		def fill_led_cmd_send_list(led_cmd, valid_cmd_list):
			led_cmd_send_list = []
			do_coap_send_led = False
			led_cmd = led_cmd.replace(" ", "")
			led_cmd_list = led_cmd.split(',')
			for cmd in led_cmd_list:
				if cmd in valid_cmd_list:
					led_cmd_send_list.append(cmd)
					do_coap_send_led = True
				else:
					led_cmd_send_list.append("x")
			return led_cmd_send_list, do_coap_send_led

		result = {'result':'ERROR', 'errors':['Failed to update']}
		led_cmd_send_list = []
		do_coap_send_led = False
		logging.info('update id {} data {}'.format(id, data))
		if id != 0:
			coap_action = data.get('coap_action', None)
			if coap_action == 'led_on':
				led_cmd = data.get('led_on_cmd', 'x')
				led_cmd_send_list, do_coap_send_led = fill_led_cmd_send_list(led_cmd, ['on', 'blink'])
				data['led_on_cmd'] = ','.join(led_cmd_send_list)
			elif coap_action == 'led_off':
				led_cmd = data.get('led_off_cmd', 'x')
				led_cmd_send_list, do_coap_send_led = fill_led_cmd_send_list(led_cmd, ['off'])
				data['led_off_cmd'] = ','.join(led_cmd_send_list)
			else:
				pass
			coap_result = {}
			if do_coap_send_led:
				try:
					ipv6_addr = data.get('ipv6', 'fec0::1')
					coap_result = coap_client.send_led(ipv6_addr, led_cmd_send_list)
					logging.info("coap_result: {}.".format(coap_result))
					if coap_result['result'] == 'OK':
						data['coap_action'] = '{}_ok'.format(coap_action)
					else:
						data['coap_action'] = '{}_err'.format(coap_action)
				except Exception as e:
					data['coap_action'] = '{}_err'.format(coap_action)
					coap_result = {'result':'ERROR', 'errors':['Exception: {}'.format(e)]}
					logging.error('Error: {}'.format(e))
			update_result = super().update(id, data)
			errors = []
			errors.extend(update_result.get('errors', []))
			errors.extend(coap_result.get('errors', []))
			logging.info('errors: {} {}.'.format(errors, type(errors)))
			if len(errors) != 0:
				result = {'result':'ERROR', 'errors':errors}
			else:
				result = {'result':'OK'}
		else:
			with self.connection:
				cursor = self.connection.cursor()
				cursor.execute("SELECT * FROM {0} WHERE(serial='{1}');".format(self.objName, data["serial"]))
				field_names = list(map(lambda x: x[0], cursor.description))
				rows = cursor.fetchall()
				# print('rows {} self.objName {}'.format(rows, self.objName))
				# logging.info('rows {} self.objName {}'.format(rows, self.objName))
				if (len(rows) == 0):
					# Create new record
					# print('create new record {} {}'.format(self.objName, data))
					result = super().create(data)
				else:
					record = {}
					for row in rows:
						field_i = 0
						for field in field_names:
							record[field] = row[field_i]
							field_i += 1
					result = super().update(record['id'], data)
		# print('result {}'.format(result))
		logging.info('result {}'.format(result))
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
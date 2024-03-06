import asyncio
import threading
import json
import logging
import time
from aiocoap import *
from aiocoap import PUT
from aiocoap.message import Message

class coap_client:
    result = None
    @classmethod
    async def coap_send(cls, coap_uri, payload_dict):
        """Perform a single PUT request to localhost on the default port, URI
        "/other/block". The request is sent 2 seconds after initialization.
        The payload is bigger than 1kB, and thus sent as several blocks."""

        logging.info('coap_uri {} payload_dict {}'.format(coap_uri, payload_dict))
        context = await Context.create_client_context()

        # await asyncio.sleep(2)
        payload = json.dumps(payload_dict).encode('utf-8')
        # print('payload {} type {}'.format(payload, type(payload)))
        logging.info('payload {} type {}'.format(payload, type(payload)))
        # coap_uri = "coap://[{0}]/{1}".format(ipv6_addr, topic)
        request = Message(code=PUT, payload=payload, uri=coap_uri)
        response = await context.request(request).response
        # print('Result: %s\n%s'%(response.code, response.payload.decode('utf-8')))
        logging.info('Result: -{}-{}'.format(str(response.code), response.payload.decode('utf-8')))
        if str(response.code) == '2.03 Valid':
            cls.result = {'result':'OK'}
            logging.info('Result: {}'.format(cls.result))
        else:
            cls.result = {'result':'ERROR', 'errors':['Wrong response code: {}'.format(response.code)]}
            logging.info('Result: {}'.format(cls.result))

    @classmethod
    async def entrypoint(cls, *args, **kwargs):
        # Wait for at most 1 second
        cls.result = {'result':'ERROR', 'errors':['Coap TimeoutError']}
        try:
            await asyncio.wait_for(cls.coap_send(*args, **kwargs), timeout=1.0)
        except asyncio.exceptions.TimeoutError:
            logging.error('COAP TimeoutError')
            cls.result = {'result':'ERROR', 'errors':['Coap TimeoutError']}
        except:
            logging.error('COAP Exception')
            cls.result = {'result':'ERROR', 'errors':['Coap Exception']}


    @classmethod
    def run_async(cls, coap_uri, payload_dict):
        # ipv6_addr = kwargs.get('ipv6_addr')
        # led_cmd_list_send = kwargs.get('led_cmd_list_send')
        _thread = threading.Thread(target=asyncio.run, args=(cls.entrypoint(coap_uri=coap_uri, payload_dict=payload_dict),))
        _thread.start()
        _thread.join()

    @classmethod
    def send_led(cls, ipv6_addr, led_list):
        """Perform a single PUT request on the default port"""
        logging.info('ipv6_addr {} led_list {}'.format(ipv6_addr, led_list))
        coap_uri = "coap://[{0}]/controldata".format(ipv6_addr)
        payload_dict = {}
        payload_dict['ctrltype'] = 'led'
        payload_dict['value'] = led_list
        cls.run_async(coap_uri, payload_dict)
        return cls.result

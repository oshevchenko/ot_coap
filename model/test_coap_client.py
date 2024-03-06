import sys
import time
import unittest
from unittest.mock import patch, MagicMock
from coap_client import coap_client
import logging

class TestCoapClient(unittest.TestCase):
    def setUp(self):
        self.client = coap_client()

    @patch('aiocoap.Context.create_client_context')
    @patch('aiocoap.Message')
    @unittest.skip("Skipping test_coap_send")
    async def test_coap_send(self, mock_Message, mock_create_client_context):
        mock_context = MagicMock()
        mock_create_client_context.return_value = mock_context

        mock_response = MagicMock()
        mock_context.request.return_value.response = mock_response

        coap_uri = 'coap://localhost/other/block'
        payload_dict = {'key': 'value'}

        await self.client.coap_send(coap_uri, payload_dict)

        mock_create_client_context.assert_called_once()
        mock_Message.assert_called_once_with(code=coap_client.PUT, payload=b'{"key": "value"}', uri=coap_uri)
        mock_context.request.assert_called_once_with(mock_Message.return_value)
        mock_response.code.assert_called_once()
        mock_response.payload.decode.assert_called_once_with('utf-8')

    # @patch('threading.Thread')
    # @patch('asyncio.run')
    # @unittest.skip("Skipping test_coap_send")
    def test_run_async(self):
        coap_uri = 'coap://[fd22:11f9:7dd5:1:a796:8a2a:3f61:33aa]/controldata'
        # coap_uri = 'coap://[fd22:11f9:7dd5:1:a796:8a2a:3f61:3300]/controldata'
        payload_dict = {'ctrltype': 'led', 'value': ['x', 'off']}
        # payload_dict = {'ctrltype': 'led', 'value': ['x', 'on']}

        coap_client.run_async(coap_uri, payload_dict)

        # mock_run.assert_called_once_with(self.client.coap_send(coap_uri=coap_uri, payload_dict=payload_dict))
        # mock_Thread.assert_called_once_with(target=mock_run.return_value, args=(self.client.coap_send.return_value,))
        # mock_Thread.return_value.start.assert_called_once()

    @patch('coap_client.coap_client.run_async')
    def test_send_led(self, mock_run_async):
        ipv6_addr = 'fd22:11f9:7dd5:1:a796:8a2a:3f61:33aa'
        led_list = ['x', 'on']

        coap_uri = 'coap://[fd22:11f9:7dd5:1:a796:8a2a:3f61:33aa]/controldata'
        payload_dict = {'ctrltype': 'led', 'value': ['x', 'on']}

        coap_client.send_led(ipv6_addr, led_list)

        mock_run_async.assert_called_once_with(coap_uri, payload_dict)

if __name__ == '__main__':
    log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')

    log = logging.getLogger()
    log.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(log_formatter)
    handler.setLevel(logging.INFO)
    log.addHandler(handler)
    unittest.main()

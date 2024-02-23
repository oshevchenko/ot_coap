import logging
import asyncio

from aiocoap import *
from aiocoap import GET

logging.basicConfig(level=logging.INFO)

async def main():
    protocol = await Context.create_client_context()

    request = Message(code=GET, uri='coap://localhost/keepalive')
    # request = Message(code=GET, uri='coap://localhost/other/block')
    # request = Message(code=GET, uri='coap://localhost/other/separate')
    # request = Message(code=GET, uri='coap://localhost/whoami')

    try:
        response = await protocol.request(request).response
    except Exception as e:
        print('Failed to fetch resource:')
        print(e)
    else:
        print('Result: %s\n%s'%(response.code, response.payload.decode("utf-8")))

if __name__ == "__main__":
    asyncio.run(main())

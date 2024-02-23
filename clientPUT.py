import logging
import asyncio

from aiocoap import *
from aiocoap import PUT
from aiocoap.message import Message

logging.basicConfig(level=logging.INFO)

async def main():
    """Perform a single PUT request to localhost on the default port, URI
    "/other/block". The request is sent 2 seconds after initialization.

    The payload is bigger than 1kB, and thus sent as several blocks."""

    context = await Context.create_client_context()

    await asyncio.sleep(2)
	
    # payload = b'{"id":4, "serial": "4444444444", "name": "Director clock", "ipv6": "fda1:98ec:3c8d:a291:167:99e1:b956:56ba",\
    #     "lastreport": "2024-02-23 11:10:15", "swver": "v0.0.3", "devtype": "dig. clock", "devrole": "router"}'
    payload = b'{"serial": "44443333", "name": "Director clock", "ipv6": "fda1:98ec:3c8d:a291:167:99e1:b956:56ba",\
        "lastreport": "2024-02-23 11:10:00", "swver": "v0.0.3", "devtype": "dig. clock", "devrole": "router"}'
    request = Message(code=PUT, payload=payload, uri="coap://localhost/keepalive")

    response = await context.request(request).response

    print('Result: %s\n%s'%(response.code, response.payload.decode('utf-8')))

if __name__ == "__main__":
    asyncio.run(main())

import logging
import asyncio

from aiocoap import *
from aiocoap import PUT

logging.basicConfig(level=logging.INFO)

async def main():
    """Perform a single PUT request to localhost on the default port, URI
    "/other/block". The request is sent 2 seconds after initialization.

    The payload is bigger than 1kB, and thus sent as several blocks."""

    context = await Context.create_client_context()

    await asyncio.sleep(2)

    payload = b"The quick brown fox jumps over the lazy dog.\n"
    request = Message(code=PUT, payload=payload, uri="coap://localhost/keepalive")
    # request = Message(code=PUT, payload=payload, uri="coap://localhost/other/blockss")

    response = await context.request(request).response

    print('Result: %s\n%s'%(response.code, response.payload.decode('utf-8')))

if __name__ == "__main__":
    asyncio.run(main())

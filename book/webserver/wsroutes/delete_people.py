import json
from book.google.people import GPeople
from wsrpc_aiohttp import WebSocketAsync, STATIC_DIR, WebSocketRoute


async def delete_people(socket: WebSocketAsync, *, resource_name):
    return json.dumps(await GPeople().delete_contacts(resource_name))

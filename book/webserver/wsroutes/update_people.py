from book.google.people import GPeople
from wsrpc_aiohttp import WebSocketAsync, STATIC_DIR, WebSocketRoute


async def update_people(socket: WebSocketAsync, *, data):
    data_fServer = await GPeople().get_contacts(data['resourceName'])

    data['etag'] = data_fServer['etag']

    return await GPeople().update_contacts(data['resourceName'], data, 'phoneNumbers,emailAddresses')

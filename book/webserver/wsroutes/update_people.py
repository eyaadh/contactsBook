from book.google.people import GPeople
from wsrpc_aiohttp import WebSocketAsync, STATIC_DIR, WebSocketRoute


async def update_people(socket: WebSocketAsync, *, data):
    data_fServer = await GPeople().get_contacts(data['resourceName'])
    org_update = data['organizations'][1]['value']

    data['etag'] = data_fServer['etag']
    data['organizations'] = data_fServer['organizations']
    data['organizations'][0]['title'] = org_update

    return await GPeople().update_contacts(data['resourceName'], data, 'phoneNumbers,emailAddresses,organizations')

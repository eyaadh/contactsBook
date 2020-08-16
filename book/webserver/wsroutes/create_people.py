from book.google.people import GPeople
from wsrpc_aiohttp import WebSocketAsync, STATIC_DIR, WebSocketRoute


async def create_people(socket: WebSocketAsync, *, data):

    """
    formulate google accepted type data
    """
    names = []
    if data['family_name'] != '' and data['given_name'] != '':
        names.append({
            'familyName': data['family_name'],
            'givenName': data['given_name']
        })
    elif data['family_name'] == '':
        names.append({
            'givenName': data['given_name']
        })
    else:
        names.append({
            'familyName': data['family_name']
        })

    phone_numbers = []
    if data['mobile'] != '':
        phone_numbers.append({
            'value': data['mobile'],
            'type': 'mobile'
        })

    if data['pager'] != '':
        phone_numbers.append({
            'value': data['pager'],
            'type': 'pager'
        })

    if data['extension'] != '':
        phone_numbers.append({
            'value': data['extension'],
            'type': 'Telephone Extension'
        })

    emails = []
    if data['work_email'] != '':
        emails.append({
            'value': data['work_email'],
            'type': 'work'
        })

    if data['personal_email'] != '':
        emails.append({
            'value': data['personal_email'],
            'type': 'other'
        })

    organizations = []
    if data['work_name'] != '' and data['title'] != '':
        organizations.append({
            'name': data['work_name'],
            'title': data['title']
        })
    elif data['work_name'] == '' and data['title'] == '':
        organizations.append({
            'name': 'VAKKARU MALDIVES',
        })
    elif data['work_name'] == '' and data['title'] != '':
        organizations.append({
            'name': 'VAKKARU MALDIVES',
            'title': data['title']
        })

    contact_dict = {
        'names': names,
        'phoneNumbers': phone_numbers,
        'emailAddresses': emails,
        'organizations': organizations
    }

    return await GPeople().create_contacts(contact_dict)

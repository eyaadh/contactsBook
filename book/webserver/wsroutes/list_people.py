import json
from book.google.people import GPeople
from wsrpc_aiohttp import WebSocketAsync, STATIC_DIR, WebSocketRoute


async def list_people(socket: WebSocketAsync):
    people = await GPeople().list_contacts()
    contacts = []
    for person in people:

        # formulate the keys as we want for phone numbers dumping unwanted
        try:
            phone_numbers = []
            for x in range(len(person["phoneNumbers"])):
                phone_numbers.append(
                    {"value": person["phoneNumbers"][x]["canonicalForm"] if "canonicalForm" in person["phoneNumbers"][x] else person["phoneNumbers"][x]["value"]
                        , "type": person["phoneNumbers"][x]["type"]}
                )
            phone_key = {
                "len": len(person["phoneNumbers"]),
                "phoneNumbers": phone_numbers
            }
        except KeyError as x:
            phone_key = {
                "len": 0,
                "phoneNumbers": []
            }

        try:
            emails = []
            for x in range(len(person["emailAddresses"])):
                emails.append(
                    {"value": person["emailAddresses"][x]["value"], "type": person["emailAddresses"][x]["type"]}
                )
            emails_key = {
                "len": len(person["emailAddresses"]),
                "emails": emails
            }

        except KeyError as x:
            emails_key = {
                "len": 0,
                "emails": []
            }

        try:
            org = person["organizations"][0]["title"]
        except KeyError:
            org = ""

        person_key = {
            "resourceName": person["resourceName"],
            "name": person["names"][0]["displayName"],
            "title": org,
            "contactNumbers": phone_key,
            "emailsAddresses": emails_key
        }

        contacts.append(person_key)

    contacts_dict = {
        "len": len(contacts),
        "contacts": contacts
    }

    contacts_json_dump = json.dumps(contacts_dict)
    return contacts_json_dump

from book.google import google_auth


class GPeople:
    def __init__(self):
        self.service = google_auth()

    async def list_contacts(self):
        results = self.service.people().connections().list(
            resourceName='people/me',
            pageSize=1000,
            personFields='names,emailAddresses,phoneNumbers,organizations').execute()
        connections = results.get('connections', [])

        return connections

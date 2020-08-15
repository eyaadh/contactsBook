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

    async def get_contacts(self, resource_name):
        results = self.service.people().get(
            resourceName=resource_name,
            personFields='names,emailAddresses,phoneNumbers,organizations').execute()

        return results

    async def delete_contacts(self, resource_name):
        results = self.service.people().deleteContact(resourceName=resource_name).execute()

        return results

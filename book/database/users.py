from passlib.hash import pbkdf2_sha256
from book.database import DB


class Users:
    def __init__(self):
        self.collection = DB().user_collection
        self.query = DB().query

    async def get_users(self):
        users = []
        documents = self.collection.all()
        for document in documents:
            users.append(
                {
                    'user_id': document['user_id'],
                    'name': document['name'],
                    'password': document['password'],
                    'groups': document['groups']
                }
            )

        return users

    async def get_user(self, user_name):
        return self.collection.search(self.query.user_id == user_name)

    async def init_db(self):
        default_pass_hash = pbkdf2_sha256.hash("password")
        default_pass2_hash = pbkdf2_sha256.hash("password2")
        if not self.collection.search(self.query.user_id == 'admin'):
            self.collection.insert(
                {
                    'user_id': 'admin',
                    'hash': default_pass_hash,
                    'groups': 'admin'
                }
            )
            self.collection.insert(
                {
                    'user_id': 'user',
                    'hash': default_pass2_hash,
                    'groups': 'user'
                }
            )


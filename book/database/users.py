from passlib.hash import pbkdf2_sha256
from book.database import DB
from tinydb.operations import set


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

    async def update_user_pass(self, user_name, password):
        password_hashed = pbkdf2_sha256.hash(password)
        self.collection.update(set('hash', password_hashed), self.query.user_id == user_name)

    async def update_user_group(self, user_name, groups):
        self.collection.update(set('groups', groups), self.query.user_id == user_name)

    async def create_new_user(self, user_name, password, group):
        password_hashed = pbkdf2_sha256.hash(password)
        if not self.collection.search(self.query.user_id == user_name):
            self.collection.insert(
                {
                    'user_id': user_name,
                    'hash': password_hashed,
                    'groups': group
                }
            )
            return True
        else:
            return False

    async def remove_user(self, user_name):
        self.collection.remove(self.query.user_id == user_name)

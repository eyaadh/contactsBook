from pathlib import Path
from tinydb import TinyDB, Query


class DB:
    def __init__(self):
        self.db = TinyDB(Path("book/working_dir/db.json"))
        self.user_collection = self.db.table("user")
        self.query = Query()

from tinydb import TinyDB

_db = None

def db_client():
    global _db
    if _db is None:
        _db = TinyDB('../db.json')
    return _db
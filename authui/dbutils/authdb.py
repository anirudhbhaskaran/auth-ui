import datetime
import os
import random
import sqlite3
import string
from urllib.parse import quote_plus


def generate_random_string(length):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(length))


class AuthDb:

    # DB Structure - AUTHY
    # id - Primary ID Key
    # clientId - Client ID
    # clientKey - Client Key
    # clientSecret - Client Secret

    con = None
    def __init__(self):
        pass

    @staticmethod
    def _get_con():
        if not AuthDb.con:
            AuthDb.con = sqlite3.connect(os.environ.get("AUTH_DB_LOCATION", "authserver.db"), check_same_thread=False)
            cur = AuthDb.con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS '{}' (id INTEGER PRIMARY KEY AUTOINCREMENT, clientId varchar(64), clientKey varchar(64), clientSecret varchar(128));".format(os.environ.get("AUTH_DB_TABLE", "AUTHY")))
            AuthDb.con.commit()
        return AuthDb.con
    
    def _get_all_auths(self):
        cur = self._get_con().cursor()
        res = cur.execute("SELECT * FROM {};".format(os.environ.get("AUTH_DB_TABLE", "AUTHY")))
        return res.fetchall()


    def _delete_auth(self, client_id):
        cur = self._get_con().cursor()
        res = cur.execute("DELETE FROM {} WHERE clientId='{}';".format(os.environ.get("AUTH_DB_TOKEN_TABLE", "AUTHY"), quote_plus(client_id)))
        self._get_con().commit()
        return
    
    def _insert_new_auth(self):
        client_id = generate_random_string(64)
        client_key = generate_random_string(64)
        client_secret = generate_random_string(128)
        cur = self._get_con().cursor()
        cur.execute("INSERT INTO {} (clientId, clientKey, clientSecret) VALUES('{}', '{}', '{}');".format(os.environ.get("AUTH_DB_TOKEN_TABLE", "AUTHY"), quote_plus(client_id), quote_plus(client_key), quote_plus(client_secret)))
        self._get_con().commit()
        return

    @staticmethod
    def _close_con():
        if AuthDb.con:
            AuthDb.con.close()
        AuthDb.con = None

import os
import re
import sqlite3

SQLITE_PATH = os.path.join(os.path.dirname(__file__), 'database.db')

class Database:

    def __init__(self):
        self.conn = sqlite3.connect(SQLITE_PATH)

    def select(self, sql, parameters=[]):
        c = self.conn.cursor()
        c.execute(sql, parameters)
        return c.fetchall()

    def execute(self, sql, parameters=[]):
        c = self.conn.cursor()
        c.execute(sql, parameters)
        self.conn.commit()

    def create_palette(self, uid, name, c1, c2, c3, c4, c5, c6, image):
        self.execute('INSERT INTO palettes (uid, name, c1, c2, c3, c4, c5, c6, image) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                     [uid, name, c1, c2, c3, c4, c5, c6, image])

    def get_palettes(self):
        data = self.select(
            'SELECT * FROM palettes')
        return [{
            'uid': d[0],
            'name': d[1],
            'c1': d[2],
            'c2': d[3],
            'c3': d[4],
            'c4': d[5],
            'c5': d[6],
            'c6': d[7],
            'image' : d[8]
        } for d in data]

    def get_total_palette_count(self):
        data = self.select('SELECT COUNT(*) FROM palettes')
        return data[0][0]

    def get_user_palettes(self, user_id):
        data = self.select(
            'SELECT * FROM palettes WHERE "uid"=? ', [user_id])
        return [{
            'uid': d[0],
            'name': d[1],
            'c1': d[2],
            'c2': d[3],
            'c3': d[4],
            'c4': d[5],
            'c5': d[6],
            'c6': d[7],
            'image' : d[8]
        } for d in data]

    def update_palette_name(self, uid, value):
        self.execute('UPDATE palettes SET name=? WHERE uid=?', [value, uid])

    def create_user(self, name, username, encrypted_password, photo):
        data = self.select('SELECT COUNT(*) FROM users')
        count = data[0][0] + 1
        self.execute('INSERT INTO users (user_id, name, username, encrypted_password, photo) VALUES (?, ?, ?, ?, ?)',
                     [count, name, username, encrypted_password, photo])

    def get_user(self, user_id):
        data = self.select('SELECT * FROM users WHERE user_id=?', [user_id])
        if data:
            d = data[0]
            return {
                'user_id': d[0],
                'name': d[1],
                'username': d[2],
                'encrypted_password': d[3],
                'photo': d[4]
            }
        else:
            return None

    def get_all_users(self):
        data = self.select('SELECT * FROM users')
        if data:
            d = data[0]
            return {
                'user_id': d[0],
                'name': d[1],
                'username': d[2],
            }
        else:
            return None

    def get_user_username(self, username):
        data = self.select('SELECT * FROM users WHERE username=?', [username])
        if data:
            d = data[0]
            return {
                'user_id': d[0],
                'name': d[1],
                'username': d[2],
                'encrypted_password': d[3],
                'photo': d[4]
            }
        else:
            return None

    def update_user_name(self, name, uid):
        self.execute('UPDATE users SET name=? WHERE user_id=?', [name, uid])

    def update_user_photo(self, photo, uid):
        self.execute('UPDATE users SET photo=? WHERE user_id=?', [photo, uid])

    def close(self):
        self.conn.close()

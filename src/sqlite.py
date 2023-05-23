import sqlite3 as sql
import threading
from flask import jsonify


local = threading.local()


class Gallery:

    def __init__(self) -> None:
        self.db_path = 'database.db'

    def get_db_connection(self):
        if not hasattr(local, 'connection'):
            local.connection = sql.connect(self.db_path)
        return local.connection

    def get_cursor(self):
        if not hasattr(local, 'cursor'):
            local.cursor = self.get_db_connection().cursor()
        return local.cursor

    def create_table(self):

        cursor = self.get_cursor()

        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS gallery(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        price REAL NOT NULL,
                        s3_id TEXT NOT NULL,
                        category TEXT NOT NULL
                    )
                    ''')
        self.get_db_connection().commit()

    def upload_to_db(self, **kwargs):

        cursor = self.get_cursor()
        cursor.execute('''
                        INSERT INTO gallery (title,price,s3_id,category)
                        VALUES (?,?,?,?)
                        ''', (kwargs['title'], kwargs['price'], kwargs['image'], kwargs['category']))
        self.get_db_connection().commit()
        return "Image Success"


# debuging

    def delete_section(self):

        cursor = self.get_cursor()
        cursor.execute("DELETE FROM gallery WHERE category = 'Test'")
        self.get_db_connection().commit()

# function used for debugging
    def show_table_entire(self):

        cursor = self.get_cursor()
        cursor.execute('SELECT * FROM gallery')
        rows = cursor.fetchall()
        self.get_db_connection().commit()
        return rows

    def retreive_images(self):
        cursor = self.get_cursor()
        cursor.execute("SELECT * FROM gallery WHERE category != 'Test'")
        rows = cursor.fetchall()

        objects = []

        for row in rows:
            obj = {
                'id': row[0],
                'title': row[1],
                'price': row[2],
                's3_id': row[3],
                'category': row[4]
            }
            objects.append(obj)
        self.get_db_connection().commit()
        return jsonify(objects)

"""
Keyword arguments:
argument -- description
Return: return_description
"""

import threading
import psycopg2
from flask import jsonify
from dotenv import load_dotenv
import os

local = threading.local()


load_dotenv()


class Gallery:

    def __init__(self) -> None:
        # Easier to have it stored in a dictionary
        self.db = {

            'host': os.getenv('DB_HOST'),
            'port': os.getenv('DB_PORT'),
            'dbname': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD')
        }

    def get_db_connection(self):
        if not hasattr(local, 'connection'):
            local.connection = psycopg2.connect(**self.db)
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

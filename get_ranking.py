import sqlite3

with sqlite3.connect('discord_db') as connection:
    cursor = connection.cursor()

    cursor.execute('select * from Post')

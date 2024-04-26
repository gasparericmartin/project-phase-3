import sqlite3

CONN = sqlite3.connect('mma_records.db')
CURSOR = CONN.cursor()

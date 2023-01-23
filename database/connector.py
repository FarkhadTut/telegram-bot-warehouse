import os
import sqlite3

db_name = 'db.sqlite3'
# os.chdir("..")

db_path = os.path.join(os.getcwd(), db_name)   
print(db_path)
con = sqlite3.connect(db_path, check_same_thread=False)

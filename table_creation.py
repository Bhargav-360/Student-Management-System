#table creation

from sqlite3 import *

con = None

try:
    con = connect("student_record.db")   #road
    print("connected")
    cursor = con.cursor()      #vechicle
    sql = "create table student_record(rno int primary key , name text , marks int)"
    cursor.execute(sql)      #passenger
    print("table created")

except Exception as e:
    print("issue" , e)

finally:
    if con is not None:
        con.close()              #close connection


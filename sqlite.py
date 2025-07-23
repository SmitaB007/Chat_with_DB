import sqlite3 

connection = sqlite3.connect("student.db")

cursor = connection.cursor()

table_info = """
create table Student_info(
Name varchar(25),
class varchar(25),
sec varchar(25),
marks varchar(25)
)
"""
cursor.execute(table_info)

cursor.execute('''
INSERT INTO Student_info values ('smita','AI','A','9.2')
''')

cursor.execute('''
INSERT INTO Student_info values ('deeksha','IT','A','9.8')
''')

cursor.execute('''
INSERT INTO Student_info values ('khushi','DS','A','9.5')
''')

cursor.execute('''
INSERT INTO Student_info values ('John','DS','B','7.0')
''')

cursor.execute('''
INSERT INTO Student_info values ('John','AI','B','7.0')
''')

print("The inserted records are")

data = cursor.execute(''' 
select * from Student_info
''')

for i in data:
    print(i)


connection.close()

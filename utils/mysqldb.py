import mysql.connector

mydb = mysql.connector.connect( # 数据连接变量
  host="localhost",
  user="root",
  passwd="root",
  database="course_manage_db" # 填写使用的数据库
)

myCursor = mydb.cursor()  # 数据库执行便量
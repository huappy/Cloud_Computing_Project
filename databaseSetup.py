import mysql.connector

mydb = mysql.connector.connect(
  host="project-database.cciooaq0e4do.us-east-1.rds.amazonaws.com",
  user="huappyDee",
  password="MasterPassword14",
  database="project-database"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE customers (name VARCHAR(255), address VARCHAR(255))")
import mysql.connector

dataBase = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'Gswarrior3',
)

# prepare a cursor object
cursorObject = dataBase.cursor()

cursorObject.execute("CREATE DATABASE elderco4")

print("All done!")
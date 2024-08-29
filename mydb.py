import mysql.connector

dataBase = mysql.connector.connect(
    host = 'database-1.cvui4ccaimm7.us-east-1.rds.amazonaws.com',
    user = 'jimmy',
    passwd = 'Gswarrior3!',
)

# prepare a cursor object
cursorObject = dataBase.cursor()

cursorObject.execute("CREATE DATABASE elderco4")

print("All done!")
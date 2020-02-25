import mysql.connector
import config

conn = mysql.connector.connect(
  host='localhost',
  user=config.username,
  passwd=config.passwd,
  auth_plugin='mysql_native_password'
)

DATABASE = 'BART_DATABASE'

initDB = f'''
  DROP DATABASE IF EXISTS {DATABASE};
  CREATE DATABASE {DATABASE};
  USE {DATABASE};
  CREATE TABLE T_BART_STATION (
    ID INT NOT NULL PRIMARY KEY,
    NAME VARCHAR(64),
    CODE VARCHAR(4)
  );
  CREATE TABLE T_RIDERSHIP (
    ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    MONTH INT,
    YEAR INT,
    ENTRY_STATION_ID INT,
    EXIT_STATION_ID INT,
    COUNT INT
  );
'''

mycursor = conn.cursor()
try:
  mycursor.execute(initDB)
except mysql.connector.Error as err:
    print(err)
    print("Error Code:", err.errno)
    print("SQLSTATE", err.sqlstate)
    print("Message", err.msg)
conn.close()
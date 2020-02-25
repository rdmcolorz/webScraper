import mysql.connector
import config

conn = mysql.connector.connect(
  host='localhost',
  user=config.username,
  passwd=config.passwd,
  auth_plugin='mysql_native_password'
)

DATABASE = 'CA_CAOCH_PENSION'

initDB = f'''
  DROP DATABASE IF EXISTS {DATABASE};
  CREATE DATABASE {DATABASE};
  USE {DATABASE};
  CREATE TABLE T_PERSON (
    ID INT NOT NULL PRIMARY KEY,
    NAME VARCHAR(64)
  );
  CREATE TABLE T_EMPLOYER (
    ID INT NOT NULL PRIMARY KEY,
    NAME VARCHAR(64)
  );
  CREATE TABLE T_EMPLOYMENT (
    ID INT NOT NULL PRIMARY KEY,
    TITLE VARCHAR(64),
    EMPLOYER_ID INT
  );
  CREATE TABLE T_PENSION (
    ID INT NOT NULL PRIMARY KEY,
    NAME VARCHAR(64)
  );
  CREATE TABLE T_PENSION_DETAIL (
    ID INT NOT NULL PRIMARY KEY,
    EMPLOYMENT_ID INT,
    PENSION_ID INT,
    PENSION_VALUE INT,
    YEARS_OF_SERVICE NUMERIC,
    YEAR_OF_RETIREMENT INT
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
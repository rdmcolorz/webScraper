import mysql.connector
import config

def connectorErrors(err):
  print(err)
  print("Error Code:", err.errno)
  print("SQLSTATE", err.sqlstate)
  print("Message", err.msg)

def DBexecuteMany(database, sql, values):
  conn = mysql.connector.connect(
    host='localhost',
    user=config.username,
    passwd=config.passwd,
    auth_plugin='mysql_native_password',
    database=database
  )
  mycursor = conn.cursor()
  try:
    mycursor.executemany(sql, values)
    conn.commit()
  except mysql.connector.Error as err:
    connectorErrors(err)
  conn.close()

def DBexecute(database, sql):
  conn = mysql.connector.connect(
    host='localhost',
    user=config.username,
    passwd=config.passwd,
    auth_plugin='mysql_native_password',
    database=database
  )
  mycursor = conn.cursor()
  try:
    mycursor.execute(sql)
    conn.commit()
  except mysql.connector.Error as err:
    connectorErrors(err)
  conn.close()


def DBinit(database, sql):
  conn = mysql.connector.connect(
    host='localhost',
    user=config.username,
    passwd=config.passwd,
    auth_plugin='mysql_native_password',
    database=database
  )
  mycursor = conn.cursor()
  try:
    mycursor.execute(sql)
  except mysql.connector.Error as err:
    connectorErrors(err)
  conn.close()

def DBquery(database, sql):
  conn = mysql.connector.connect(
    host='localhost',
    user=config.username,
    passwd=config.passwd,
    auth_plugin='mysql_native_password',
    database=database
  ) 
  mycursor = conn.cursor()
  try:
    mycursor.execute(sql)
    results = mycursor.fetchall()
  except mysql.connector.Error as err:
    connectorErrors(err)
  conn.close()
  return results
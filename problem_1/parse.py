import requests
import pandas as pd
import xlrd
import os
from helper import DBexecuteMany, queryDB

currPath = os.getcwd()
DATABASE = 'BART_DATABASE'
abbrevPath = currPath + '/Station_Names.xls'

def parseFile(df):
  values = []
  for exitID, row in df.iterrows():
    for entryID, count in zip(row.index.tolist(), row.values.tolist()):
      values.append((entryID, exitID, count))
  return values

def parseFile2DB(database, year, month, fileLocation):
  print('Parsing: ', year, month, fileLocation)
  df = pd.read_excel(fileLocation, 
                      sheet_name='Total Trips OD', 
                      header=1, 
                      ).set_index('Unnamed: 0')
  df = df.iloc[:-1, :-1]
  df.columns = df.columns.astype(str)
  df = df.rename(columns=abbrevMapping, index=abbrevMapping)
  values = parseFile(df)
  sql = "INSERT INTO T_RIDERSHIP \
          (MONTH, YEAR, ENTRY_STATION_ID, EXIT_STATION_ID, COUNT) \
          VALUES ({0}, {1}, %s, %s, %s);".format(year, month)
  DBexecuteMany(database, sql, values)

# get abbrev codings
abbrev = queryDB(DATABASE, 'SELECT CODE, ID FROM T_BART_STATION')
abbrevMapping = dict(abbrev)

df = pd.read_json(currPath + '/bartMeta.json', orient='index')
df.apply(lambda row: parseFile2DB(DATABASE, 
                                    row['year'], 
                                    row['month'], 
                                    row['fileLocation']
                                    ), axis=1)
import requests
import pandas as pd
import os
import numpy as np
from helper import DBexecuteMany

currPath = os.getcwd()
DATABASE = 'BART_DATABASE'

bartAbbrev = 'https://www.bart.gov/sites/default/files/docs/Station_Names.xls'
abbrev = requests.get(bartAbbrev)
abbrevPath = currPath + '/Station_Names.xls'

def populate():
  with open(abbrevPath, 'wb') as f:
    f.write(abbrev.content)
  df = pd.read_excel(abbrevPath)
  values = list(zip(df.index.values.tolist(), df.iloc[:, 1], df.iloc[:, 2]))

  # found missing values in station abbbreviations
  abbrevdf = pd.read_excel(abbrevPath)
  abbrevMapping = dict(zip(abbrevdf.iloc[:, 1], abbrevdf.index.values))
  testdf = pd.read_excel(currPath + '/bartMonthly/Ridership_201901.xlsx', 
                        sheet_name='Total Trips OD', 
                        header=1, 
                        ).set_index('Unnamed: 0')

  abbrevCode = list(abbrevdf.iloc[:, 1])
  checkMissing = [x for x in testdf if x not in abbrevCode][:-1]
  print(f'Missing values : {checkMissing}')

  # TODO: make getting missing values easier...hardcoding right now.
  missing = [(46, 'ML', 'Milpitas'), 
  (47, 'BE', 'Berryessa'), 
  (48, 'PC', 'Pittsburg Center'), 
  (49, 'AN', 'Antioch')]

  values = values + missing
  print(f'Added missing values by hand...\n{missing}')
  fillStationAbbrev = "INSERT INTO T_BART_STATION \
                        (ID, CODE, NAME) VALUES (%s, %s, %s);"
  DBexecuteMany(DATABASE, fillStationAbbrev, values)

if __name__ == '__main__':
  populate()
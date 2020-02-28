import requests
import os
from bs4 import BeautifulSoup
import pandas as pd
from helper import DBexecuteMany, DBquery, DBexecute, DBinit

currPath = os.getcwd()
DATABASE = 'CA_COACH_PENSION'

# create temp table to store all data from html
createTemp = '''DROP TABLE IF EXISTS T_TEMP;
                    CREATE TABLE T_TEMP (
                    ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    NAME VARCHAR(64),
                    TITLE VARCHAR(64),
                    EMPLOYER VARCHAR(64),
                    PENSION VARCHAR(64),
                    PENSION_VALUE INT,
                    BENEFITS VARCHAR(64),
                    DISABILITY VARCHAR(64),
                    YEARS_OF_SERVICE INT,
                    YEAR_OF_RETIREMENT INT,
                    TOTAL_PENSION INT)
                  '''
DBinit(DATABASE, createTemp)

# start parsing html files from folder
df = pd.read_json(currPath + '/caCoachPension.json', orient='index')
for html in df['fileLocation']:
  with open(html, 'r') as f:
    htmlFile = f.read()
  
  soup = BeautifulSoup(htmlFile, features='lxml')
  rows = soup.find_all('tr')

  # start parsing table
  pageData = []
  for row in rows:
    columns = row.find_all('td')
    columnData = []
    for column in columns:
      if ':' in column.text and '(' not in column.text:
        form = {'Title': '', 'Employer': '', 'Pension': ''}
        ele = column.text.split('\n')
        ele = dict([item.strip().split(': ') for item in ele if item.strip() != ''])
        form['Title'] = ele.get('Title', 'N/A')
        form['Employer'] = ele.get('Employer', 'N/A')
        form['Pension'] = ele.get('Pension', 'N/A')
        columnData.append(form)
      else: 
        columnData.append(column.text.strip().title().split('\n')[0])
    if columnData:
      pageData.append(columnData)

  values = []
  for row in pageData:
    values.append((row[0], row[1]['Title'], row[1]['Employer'], row[1]['Pension'],
                    ''.join(row[2][1:-3].split(',')), row[3], 
                    row[4], row[5], row[6], ''.join(row[7][1:-3].split(','))))

  sql = '''INSERT IGNORE INTO T_TEMP \
            (NAME, TITLE, EMPLOYER, PENSION, PENSION_VALUE, BENEFITS, DISABILITY, \
              YEARS_OF_SERVICE, YEAR_OF_RETIREMENT, TOTAL_PENSION) VALUES \
              (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        '''
  DBexecuteMany(DATABASE, sql, values)

# extract data into individual tables using T_TEMP
# populate T_PERSON
sql = "INSERT INTO T_PERSON (NAME) SELECT DISTINCT NAME FROM T_TEMP;"
DBexecute(DATABASE, sql)

# populate T_EMPLOYER
sql = "INSERT INTO T_EMPLOYER (NAME) SELECT DISTINCT EMPLOYER FROM T_TEMP"
DBexecute(DATABASE, sql)

# populate T_PENSION
sql = "INSERT INTO T_PENSION (NAME) SELECT DISTINCT PENSION FROM T_TEMP"
DBexecute(DATABASE, sql)

# populate T_EMPLOYMENT
sql = "INSERT INTO T_EMPLOYMENT (TITLE, PERSON_ID, EMPLOYER_ID) \
        SELECT DISTINCT T_TEMP.TITLE, T_PERSON.ID, T_EMPLOYER.ID \
        FROM T_TEMP \
          INNER JOIN T_PERSON ON T_TEMP.NAME = T_PERSON.NAME \
          INNER JOIN T_EMPLOYER ON T_TEMP.EMPLOYER = T_EMPLOYER.NAME;"
DBexecute(DATABASE, sql)

# populate T_PENSION_DETAIL
sql = '''INSERT INTO T_PENSION_DETAIL
            (EMPLOYMENT_ID, PENSION_ID, PENSION_VALUE, YEARS_OF_SERVICE, YEAR_OF_RETIREMENT)
          SELECT T_EMPLOYMENT.ID, TEMP_W_ID.PENSION_ID, TEMP_W_ID.PENSION_VALUE,
                  TEMP_W_ID.YEARS_OF_SERVICE, TEMP_W_ID.YEAR_OF_RETIREMENT
          FROM
            (SELECT T_TEMP.TITLE, T_EMPLOYER.ID EMPLOYER_ID, T_PERSON.ID PERSON_ID,
                    T_PENSION.ID PENSION_ID, T_TEMP.PENSION_VALUE, T_TEMP.YEARS_OF_SERVICE,
                    T_TEMP.YEAR_OF_RETIREMENT
              FROM T_TEMP
                INNER JOIN T_EMPLOYER ON T_TEMP.EMPLOYER = T_EMPLOYER.NAME
                INNER JOIN T_PERSON ON T_TEMP.NAME = T_PERSON.NAME
                INNER JOIN T_PENSION ON T_TEMP.PENSION = T_PENSION.NAME
            ) AS TEMP_W_ID
            INNER JOIN T_EMPLOYMENT ON T_EMPLOYMENT.TITLE = TEMP_W_ID.TITLE
                                    AND T_EMPLOYMENT.PERSON_ID = TEMP_W_ID.PERSON_ID
                                    AND T_EMPLOYMENT.EMPLOYER_ID = TEMP_W_ID.EMPLOYER_ID;
        '''
DBexecute(DATABASE, sql)
from helper import DBinit

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

DBinit(initDB)
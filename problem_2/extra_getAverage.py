import pandas as pd
from helper import DBquery
import json

DATABASE = 'CA_COACH_PENSION'

def getAverage():
  sql = '''SELECT pd.YEAR_OF_RETIREMENT, ROUND(AVG(pd.PENSION_VALUE) / AVG(pd.YEARS_OF_SERVICE), 2) AS AVERGE
            FROM T_PENSION_DETAIL as pd
            GROUP BY pd.YEAR_OF_RETIREMENT
            HAVING pd.YEAR_OF_RETIREMENT != 0
            ORDER BY pd.YEAR_OF_RETIREMENT ASC;
        '''
  average = DBquery(DATABASE, sql)
  df = pd.DataFrame(average, 
                    columns=['Year_of_retirement', 'Aveage_pension_PER_Years_of_service'])
  j = df.to_json('averagePension.json', orient='index')

getAverage()
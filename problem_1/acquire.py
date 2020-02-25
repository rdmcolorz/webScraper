import requests
import lxml.html
import pandas as pd
import xlrd
import os

currPath = os.getcwd()
fileDir = currPath + '/bartMonthly'

try:
  os.mkdir(fileDir)
except OSError:
  print(f'--- Creation of directory {fileDir} failed. ---')
else:
  print(f'--- Created {fileDir} ---')

bartMonthlyRidershipUrl = 'http://64.111.127.166/ridership/'

html = requests.get(bartMonthlyRidershipUrl)
doc = lxml.html.fromstring(html.content)
hrefs = doc.xpath('/html/body/pre/a/text()')
xlxsFiles = [item for item in hrefs if '.xlsx' in item]
print(xlxsFiles)

# Save ridership xlsx files to bartMonthly dir
fileLocation = []
year = []
month = []
for fileName in xlxsFiles:
  xfile = requests.get(bartMonthlyRidershipUrl + fileName)
  filePath = 'bartMonthly/' + fileName
  with open(filePath, 'wb') as f:
    f.write(xfile.content)
    print(f'--- Saved {filePath}')
    fileLocation.append(filePath)
    year.append(int(fileName[-11:-7]))
    month.append(int(fileName[-7:-5]))

df = pd.DataFrame(zip(year, month, fileLocation), 
                  columns = ['year', 'month', 'fileLocation'])
df.to_json('bartMeta.json', orient='index')
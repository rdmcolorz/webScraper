import requests
import lxml.html
import pandas as pd
import os

currPath = os.getcwd()
fileDir = currPath + '/caCoachPension/'

try:
  os.mkdir(fileDir)
except OSError:
  print(f'--- Creation of directory {fileDir} failed. ---')
else:
  print(f'--- Created {fileDir} ---')

firstPage = 'https://transparentcalifornia.com/pensions/search/?q=coach&y='
otherPages = 'https://transparentcalifornia.com/pensions/search/?q=coach&y=&page={}'


fileLocation = []
pageList = []

for page in range(1, 28):
  if page == 1:
    pageUrl = firstPage
  else:
    pageUrl = otherPages.format(str(page))

  html = requests.get(pageUrl)
  filePath = fileDir + str(page) + '.html'
  
  with open(filePath, 'wb') as f:
    f.write(html.content)
    print(f'--- Saved {filePath}')
    fileLocation.append(filePath)
    pageList.append(page)

df = pd.DataFrame(zip(pageList, fileLocation), columns = ['page', 'fileLocation'])
df.to_json('caCoachPension.json', orient='index')
    
# can't get xpath to grab data based on class, so just grab all and parse after.
# TODO: Figure out xpath attribute grab

# doesntwork = doc.xpath('.//td[@class="tablesaw-priorities-1"]')
# doc = lxml.html.fromstring(html.content)
# jobEmployerPension = doc.xpath('//td/a/text()')
# data = doc.xpath("//td/text()")
# data = [item for item in data if '\n' not in item]
# totalPension = data[0::6]
# yearOfRetirement = data[4:][0::6]
# yearsOfService = data[3:][0::6]
# print(yearOfRetirement)

# Save ridership xlsx files to bartMonthly dir
# fileLocation = []
# year = []
# month = []
# for fileName in xlxsFiles:
#   xfile = requests.get(bartMonthlyRidershipUrl + fileName)
#   filePath = 'bartMonthly/' + fileName
#   with open(filePath, 'wb') as f:
#     f.write(xfile.content)
#     print(f'--- Saved {filePath}')
#     fileLocation.append(filePath)
#     year.append(int(fileName[-11:-7]))
#     month.append(int(fileName[-7:-5]))

# df = pd.DataFrame(zip(year, month, fileLocation), 
#                   columns = ['year', 'month', 'fileLocation'])
# df.to_json('bartMeta.json', orient='index')
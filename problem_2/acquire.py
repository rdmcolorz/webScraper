import requests
import pandas as pd
import os

currPath = os.getcwd()
fileDir = currPath + '/caCoachPension/'

def p2_acquire():
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

    html = requests.get(pageUrl).text
    filePath = fileDir + str(page) + '.html'
    
    with open(filePath, 'w') as f:
      f.write(html)
      print(f'--- Saved {filePath}')
      fileLocation.append(filePath)
      pageList.append(page)

  df = pd.DataFrame(zip(pageList, fileLocation), 
                      columns = ['page', 'fileLocation'])
  df.to_json('caCoachPension.json', orient='index')

if __name__ == '__main__':
  p2_acquire()
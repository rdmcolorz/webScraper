### Assessment details:

#### - Setup a python virtual environment using venv.
#### - initDB.py for testing and setup, if you want to use this script you'll need a config file with username and password.
#### - You can find the version I uploaded to github (https://github.com/rdmcolorz/webScraper)
#### - extra_getAverage.py is bonus for Problem 2.

## Problem1:
#### - There are missing values in the abbreviation list (46 stations) to the ridership data (50 stations) so I manually looked it up and hardcoded values into the database.

## Problem2:
#### - Had trouble using lxml to get parse attribute values in problem 2 so switched to beautifulsoup. Request was not pulling in the class attribute values in the html.  
#### - Tried to use python to parse data at first and realized I can use SQL to do it faster and easier.
#### - Couldn't get json to pretty display, will look into it further.
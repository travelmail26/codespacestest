#from chefwriter import AIHandler
from perplexitychef import perplexitycall
from sheetscallchef import fetch_chatlog, fetch_preferences, fetch_chatlog_time, fetch_recipes
#from postprocess import postprocess
import pytz
from datetime import datetime
#fetch_chatlog()
#print(fetch_preferences())

#print(fetch_chatlog_time('2024-11-08T14:57:44.874244', '2024-11-08T14:57:44.874246'))
#print(fetch_chatlog_time())

def get_current_time():
  eastern = pytz.timezone('America/New_York')
  print('DEBUG: get_current_time triggered', datetime.now(eastern).strftime('%Y-%m-%d %H:%M:%S %Z'))
  return datetime.now(eastern).strftime('%Y-%m-%d %H:%M:%S %Z')

get_current_time()
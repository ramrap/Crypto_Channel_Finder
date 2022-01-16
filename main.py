

from __future__ import print_function
from locale import currency
import gate_api
from gate_api.exceptions import ApiException, GateApiException
import time
import datetime
import pandas as pd 
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mpl_dates
import matplotlib.pyplot as plt
from _util import *


# Defining the host is optional and defaults to https://api.gateio.ws/api/v4
# See configuration.py for a list of all supported configuration parameters.
configuration = gate_api.Configuration(
    host = "https://api.gateio.ws/api/v4"
)

api_client = gate_api.ApiClient(configuration)
# Create an instance of the API class
api_instance = gate_api.SpotApi(api_client)



def find_dataframe(df,currency_pair):
    levels = []
    
    
    s =  np.mean(df['high'] - df['low'])
    def isFarFromLevel(l):
        return np.sum([abs(l-x) < s  for x in levels]) == 0
    
    levels = []
    for i in range(2,df.shape[0]-2):
        if isSupport(df,i):
            l = df['low'][i]
            if isFarFromLevel(l):
                levels.append((i,l))
        elif isResistance(df,i):
            l = df['high'][i]
            if isFarFromLevel(l):
                levels.append((i,l))
                
    plot_graphs(df,levels,currency_pair)
        
        
def execute_testcase(data,limit=25):
  
    # currency_pair = 'ETH_USDT' # str | Currency pair
    currency_pair = data[0]+'_USDT'
   
    interval = data[1] # str | Interval time between data points (optional) (default to '30m')
    
    _from = convertToUnixTime(data[2])
    to = convertToUnixTime(data[3])
    
    print(datetime.datetime.utcfromtimestamp(_from).strftime('%Y-%m-%d %H:%M:%S'))
    print(datetime.datetime.utcfromtimestamp(to).strftime('%Y-%m-%d %H:%M:%S'))
    
    print(currency_pair,interval,_from,to)

    try:
        # Market candlesticks
        
        api_response = api_instance.list_candlesticks(currency_pair, interval = interval,_from= _from,to = to, limit= limit)
       
        cur_price = []
        for res in api_response:
            cur_price.append(convertToDict(res))
        df = pd.DataFrame(cur_price)
        
      
        find_dataframe(df,currency_pair)
       
            
    except GateApiException as ex:
        print("Gate api exception, label: %s, message: %s\n" % (ex.label, ex.message))
    except ApiException as e:
        print("Exception when calling SpotApi->list_candlesticks: %s\n" % e)
        

lines = []
datas = []

threshold = 25

with open('in.txt') as f:
    lines = f.readlines()
    
    numberOfTestCases = int(removeSlashN( lines[0]))
    threshold = int( removeSlashN(lines[1]))
    
    for i in range(2, len(lines)):
        line = removeSlashN(lines[i])
        data = line.split(',')
        
        data = [x.strip() for x in data]
        datas.append(data)
        
for data in datas:
    execute_testcase(data,threshold)
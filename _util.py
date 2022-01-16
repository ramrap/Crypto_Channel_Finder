import time
import datetime
import plotly.graph_objects as go


from mpl_finance import candlestick_ohlc


def removeSlashN(s):
    return s.replace('\n', '')

def convertToUnixTime(date):
    date = date.split('/')
    date = datetime.datetime(int(date[2]), int(date[0]), int(date[1]))
    return int(time.mktime(date.timetuple()))

def convertToDict(data):
    return {
        'time' : float(data[0]),
        'vol' : float(data[1]),
        'close' : float(data[2]),
        'high' : float(data[3]),
        'low' : float(data[4]), 
        'open' : float(data[5])
    }


def isSupport(df,i):
  support = df['low'][i] < df['low'][i-1]  and df['low'][i] < df['low'][i+1] and df['low'][i+1] < df['low'][i+2] and df['low'][i-1] < df['low'][i-2]
  return support
def isResistance(df,i):
  resistance = df['high'][i] > df['high'][i-1]  and df['high'][i] > df['high'][i+1] and df['high'][i+1] > df['high'][i+2] and df['high'][i-1] > df['high'][i-2]
  return resistance
    
def plot_graphs(data,levels,file_name):
    df = data
    
    _time = [ datetime.datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S') for x in df['time']]
    # print(_time)
    
    fig = go.Figure(data=[go.Candlestick(
                    x=_time,
                    open=df['open'],
                    high=df['high'],
                    low=df['low'],
                    close=df['close'])])
    max_time = _time[-1]
    for i in levels:
        fig.add_shape(type='line',
                x0=_time[i[0]],
                y0=i[1],
                x1=max_time,
                y1=i[1],
                line=dict(color='Blue',),
                xref='x',
                yref='y'
        )


    fig.show()
    fig.write_image(file_name+'.png')
    
    
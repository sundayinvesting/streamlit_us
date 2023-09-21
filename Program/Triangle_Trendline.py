import pandas as pd
from datetime import datetime
import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import linregress
from sklearn.linear_model import LinearRegression
from scipy import stats
import plotly.graph_objects as go
import streamlit as st
from PIL import Image
import requests
from io import StringIO
import yfinance as yf

token = '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'
owner = 'sundayinvesting'
repo = 'Streamlit'

database_min_length = 10
def fun_acendingtriangle(ticker,param):
    Mountain_Peak = param[1]
    global candleid
    import datetime
    #print(param[2])
    try:
        if param[0]=='Weekly':
            df = yf.download(ticker, start=param[2] - datetime.timedelta(days=2000), end=param[2], interval='1wk')
        elif param[0] == 'Daily':
            df = yf.download(ticker, start=param[2] - datetime.timedelta(days=500), end=param[2], interval='1d')
        elif param[0] == 'Hourly':
            df = yf.download(ticker, start=param[2] - datetime.timedelta(days=50), end=param[2], interval='60m')
    except:return
    #print(df)
    df = df.reset_index()
    df.rename(columns={'Date': 'date'}, inplace=True)
    df.rename(columns={'Datetime': 'date'}, inplace=True)
    #df['date']=df['date'].dt.strftime("%d/%m/%y")
    if(len(df)<database_min_length):
        return print("No Data")
    df['Ticker'] = ticker

    # df.to_csv('openbb_data.csv', index=True)
#######################################################################################
    def pivotid(df1, l, n1, n2):  # n1 n2 before and after candle l
        if l - n1 < 0 or l + n2 >= len(df1):
            return 0

        pividlow = 1
        pividhigh = 1
        for i in range(l - n1, l + n2 + 1):
            if (df1.Low[l] > df1.Low[i]):
                pividlow = 0
            if (df1.High[l] < df1.High[i]):
                pividhigh = 0
            if pividlow == 0 and pividhigh == 0:
                break
        if pividlow and pividhigh:
            return 3
        elif pividlow:
            return 1
        elif pividhigh:
            return 2
        else:
            return 0


    ################### run above function to get added pivot point column
    df['pivot'] = df.apply(lambda x: pivotid(df, x.name, 7, 7), axis=1)
    # df.to_csv('pivot.csv', index=True)

###########################################################################################
    import numpy as np
    def pointpos(x):
        if x['pivot'] == 1:
            return x['Low'] - 1e-3
        elif x['pivot'] == 2:
            return x['High'] + 1e-3
        else:
            return np.nan

    df['pointpos'] = df.apply(lambda row: pointpos(row), axis=1)

    #df.to_csv('pointpos.csv', index=True)
    #print(df)
############################################################################## Plot linear reg line
    import numpy as np
    from matplotlib import pyplot
    from scipy.stats import linregress
    # initialize arrays
    backcandles = Mountain_Peak * 4 + 5
    #backcandles=30
    for candleid in range(len(df) - 1, len(df)-5, -1):
        #print(candleid)
        maxim = np.array([])
        minim = np.array([])
        xxmin = np.array([])
        xxmax = np.array([])
        for i in range(candleid, candleid - backcandles, -1):

            if df.iloc[i].pivot == 1:
                minim = np.append(minim, df.iloc[i].Low)
                xxmin = np.append(xxmin, i)  # could be i instead df.iloc[i].name
            if df.iloc[i].pivot == 2:
                maxim = np.append(maxim, df.iloc[i].High)
                xxmax = np.append(xxmax, i)  # df.iloc[i].name

            if (xxmax.size < 2 and xxmin.size < 2) or xxmax.size == 0 or xxmin.size == 0:
                continue
        if (xxmax.size < 2 and xxmin.size < 2) or xxmax.size == 0 or xxmin.size == 0:
            continue

        slmin, intercmin, rmin, pmin, semin = linregress(xxmin, minim)
        slmax, intercmax, rmax, pmax, semax = linregress(xxmax, maxim)

        if abs(rmax) >= 0.8 and abs(rmin) >= 0.8 and slmin >= 0.00001 and slmax <= -0.00001:
            print(df)
            # print(rmin, rmax, candleid)
            print("found", df.iloc[candleid].date, df.iloc[candleid].Ticker, candleid)

            import plotly.graph_objects as go

            # Get the index of the row to use as the current period
            current_period = df.index[candleid]

            # Select the past 20 periods of data
            print(xxmin,xxmax)
            xxmax=xxmax.tolist()
            xxmin=xxmin.tolist()
            print(xxmin, xxmax)
            Index_List = xxmin + xxmax
            print(Index_List)
            Index_List.sort()

            dfpl = df[int(Index_List[0])-5:]

            #create chart
            fig = go.Figure(data=[go.Candlestick(x=dfpl.index,
                                                 open=dfpl['Open'],
                                                 high=dfpl['High'],
                                                 low=dfpl['Low'],
                                                 close=dfpl['Close'],
                                                 increasing_line_color= 'green', decreasing_line_color= 'red')])

            # Add a marker for each pivot point in the past 20 periods
            fig.add_scatter(x=dfpl.index, y=dfpl['pointpos'], mode="markers",
                            marker=dict(size=4, color="MediumPurple"),
                            name="pivot")

            xxmin = np.append(xxmin, xxmin[-1])
            xxmax = np.append(xxmax, xxmax[-1])
            fig.add_trace(go.Scatter(x=xxmin, y=slmin * xxmin + intercmin, mode='lines', name='min slope'))
            fig.add_trace(go.Scatter(x=xxmax, y=slmax * xxmax + intercmax, mode='lines', name='max slope'))
            fig.update_layout(xaxis_rangeslider_visible=False)
            fig.update_traces(showlegend=False)
            # Update x-axis to show dates
            dfpl['date'] = dfpl['date'].dt.strftime('%m-%d')
            fig.update_layout(xaxis=dict(
                tickmode='array',
                tickvals=dfpl.index,
                ticktext=dfpl['date']
            ))
            data = fig.to_image(format='jpg')
            return data

@st.cache_data
def fun_getlist(a,param):
    progress = st.progress(0, text="WIP")
    if a == "Nifty50":
        path="Directory/NSE50.csv"
    elif a == "FnO":
        path="Directory/FNO.csv"
    elif a == "NIFTY500":
        path = "Directory/NSE500.csv"

    r = requests.get(
        'https://api.github.com/repos/{owner}/{repo}/contents/{path}'.format(
            owner=owner, repo=repo, path=path),
        headers={
            'accept': 'application/vnd.github.v3.raw',
            'authorization': 'token {}'.format(token)
        }
    )

    # convert string to StringIO object
    string_io_obj = StringIO(r.text)

    # Load data to df
    script_list = pd.read_csv(string_io_obj, sep=",", index_col=0,header=None)
    script_list = script_list.reset_index()[0].values.tolist()
    print(script_list)
    i=0
    j=1
    for item2 in script_list:
        cur=script_list.index(item2)
        sumlen=len(script_list)
        progress.progress(int(round(cur/sumlen*100,0)),text="%d of %d Processed"%(cur,sumlen))
        op=fun_acendingtriangle(item2,param)
        if op == None:
            continue
        else:
            i+=1
            if i ==1:
                locals()['col'+str(j)],locals()['col'+str(j+1)]=st.columns([1,1],gap='small')
                locals()['col'+str(j)].image(op,caption=item2,use_column_width =True)
            if i==2:
                locals()['col' + str(j+1)].image(op,caption=item2,use_column_width =True)
                i=0
                j+=2
    progress.progress(100,"Extracted")
# fun_getlist("2_nasdaq script list")#
#fun_getlist("NIFTY500")
# fun_getlist("SP500")
# fun_acendingtriangle('INFY.NS')
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
    global candleid
    import datetime

    print(param[3])
    try:
        if param[0]=='Weekly':
            df = yf.download(ticker, start=param[3] - datetime.timedelta(days=2000), end=param[3], interval='1wk')
        elif param[0] == 'Daily':
            df = yf.download(ticker, start=param[3] - datetime.timedelta(days=500), end=param[3], interval='1d')
        elif param[0] == 'Hourly':
            df = yf.download(ticker, start=param[3] - datetime.timedelta(days=50), end=param[3], interval='60m')
    except:return
    #print(df)
    df = df.reset_index()
    df.columns=['date','Open','High','Low','Close','Adj.Close','Volume']
    df['date']=df['date'].dt.strftime("%d/%m/%y")
    if(len(df)<database_min_length):
        return print("No Data")
    df = df.reset_index()
    df['Ticker'] = ticker
    # df.to_csv('openbb_data.csv', index=True)
#######################################################################################
    def pivotid(df1, l, n1, n2):
        if l - n1 < 0 or l + n2 >= len(df1):
            return 0

        pividhigh = 1
        for i in range(l - n1, l + n2 + 1):
            if (df1.Low[l] > df1.Low[i]):
                pividhigh = 0
        if pividhigh:
            return 2
        else:
            return 0

    df['pivot'] = df.apply(lambda x: pivotid(df, x.name,param[2], param[2]), axis=1)
    # df.to_csv('pivot.csv', index=True)

###########################################################################################
    import numpy as np
    def pointpos(x):
        if x['pivot'] == 2:
            return x['Low'] - 1e-3
        else:
            return np.nan

    df['pointpos'] = df.apply(lambda row: pointpos(row), axis=1)
    #df.to_csv('pointpos.csv', index=True)
    print(df)
############################################################################## Plot linear reg line

    # initialize arrays
    maxim = np.array([])
    xxmax = np.array([])

    # get the index and high values of rows where pivot is equal to 2
    mask = df['pivot'] == 2
    df_temp = df[mask]
    maxim = np.append(maxim, df_temp['Low'].tail(2).values)
    xxmax = np.append(xxmax, df_temp.index[-2:])

    try:
        slmax, intercmax, rmax, pmax, semax = linregress(xxmax, maxim)
        prediction = slmax * df.index[-1] + intercmax
    except:
        return None

    # print(prediction)
    if abs(df.Close.iloc[-1] - prediction) <= param[1] * prediction:

        #plot graph
        start_index = df.index.get_loc(xxmax[0] - 20)
        dfpl = df[start_index:]

        # create chart
        fig = go.Figure(data=[go.Candlestick(x=dfpl.index,
                                             open=dfpl['Open'],
                                             high=dfpl['High'],
                                             low=dfpl['Low'],
                                             close=dfpl['Close'],
                                             increasing_line_color= 'green', decreasing_line_color= 'red')],)
        # add linear regression line
        xxmax_extended = np.array(list(range(int(xxmax[0]), int(df.index[-1]))))
        fig.add_trace(
            go.Scatter(x=xxmax_extended, y=slmax * xxmax_extended + intercmax, mode='lines', name='max slope'))
        fig.update_layout(xaxis_rangeslider_visible=False)

        #dfpl.date=dfpl.date.astype(str)
        #dfpl.apply(lambda x : x[-6:])

        # Update x-axis to show every 5th date
        tickvals = dfpl.index[::5]  # get every 5th date index
        ticktext = dfpl['date'][::5]  # get the corresponding date string
        print(ticktext,"Date")
        fig.update_layout(xaxis=dict(
            tickmode='array',
            tickvals=tickvals,
            ticktext=ticktext
        ))

        # Remove legend
        fig.update_traces(showlegend=False)

        #fig.write_image( "C:/Users/DELL/Desktop//{}.jpeg".format(ticker))
        #fig.show()
        data=fig.to_image(format='jpg')
        return data
    else:
        print("out of range")
        return None
@st.cache_data
def fun_getlist(a,param):
    progress = st.progress(0, text="WIP")
    if a == "Nifty50":
        path="Directory/NSE50.csv"
    elif a == "FnO":
        path="Directory/FNO.csv"
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

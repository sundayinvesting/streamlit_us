import datetime
import pandas as pd
import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
import requests
from io import StringIO
from stocktrends import indicators

token = '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'
owner = 'sundayinvesting'
repo = 'Streamlit'

def RSZL_Extract(ticker,param):
    #print(param)
    try:
        if param[2]=='Weekly':
            df = yf.download(ticker, start=param[3] - datetime.timedelta(days=3000),
                             end=param[3], interval='1wk')

            src = yf.download("^NSEI", start=param[3] - datetime.timedelta(days=3000),
                              end=param[3],interval='1wk')

        elif param[2] == 'Daily':
            src = yf.download("^NSEI", start=param[3] - datetime.timedelta(days=300),
                              end=param[3], interval='1d')
            df = yf.download(ticker, start=param[3]- datetime.timedelta(days=300), end=param[3], interval='1d')
        df = df.reset_index()
        #print(df)
        df.rename(columns={'Date': 'date'}, inplace=True)
        src = src.reset_index()
        src.rename(columns={'Date': 'date'}, inplace=True)
        df['date'] = df['date'].dt.strftime("%d/%m/%y")
        df['Ticker'] = ticker
        df['RS']=round(((df['Close'].shift(1)/df['Close'].shift(param[0]))/(
                                src['Close'].shift(1)/src['Close'].shift(param[0]))-1),3)
        #df.to_csv(r'C:\Users\DELL\Desktop\Temp\data.csv')
        #print(df,src)
        def condition_check(df):
            #if (df['RS'].tail(length) > 0).all():
            if (df['RS'].tail(param[1][0]) > 0).all() and (
                    df['RS'][df.index.argmax() - param[1][0] - param[1][1]:df.index.argmax() - param[1][0]+1] < 0).all():
                try:
                    df = df[df.index.argmax() - param[1][0] - param[1][1]-5:]
                    return df
                except: None
        def Plot_Gen(data):
            fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.05, row_heights=[0.7, 0.3])
            fig.add_trace(go.Candlestick(
                x=data['date'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                increasing_line_color='green', decreasing_line_color='red'), row=1, col=1)

            PSpan_Data = data[data.index.argmax() - param[1][0] +1 :]
            Trans_Data = data[data.index.argmax() - param[1][0] : data.index.argmax() - param[1][0] +2]
            NSpan_Data = data[data.index.argmax() - param[1][0] - param[1][1] : data.index.argmax() - param[1][0]+1]
            Cushion_Data = data[data.index.argmax() - param[1][0] - param[1][1]-5: \
                                data.index.argmax() - param[1][0] - param[1][1]+1]

            # Add line plot for close price to the bottom subplot
            fig.add_trace(go.Scatter(x=NSpan_Data['date'], y=NSpan_Data['RS'], name='NRS', mode='lines', line= dict(
                color='red',width=2)), row=2, col=1)
            fig.add_trace(go.Scatter(x=PSpan_Data['date'], y=PSpan_Data['RS'], name='PRS', mode='lines', line= dict(
                color='Green',width=2)), row=2, col=1)
            fig.add_trace(go.Scatter(x=Trans_Data['date'], y=Trans_Data['RS'], name='TRNRS', mode='lines+markers',
                                     line= dict(color='#00008B',width=2)), row=2, col=1)
            fig.add_trace(go.Scatter(x=Cushion_Data['date'], y=Cushion_Data['RS'], name='NRS', mode='lines', line= dict(
                color='Black',width=2)), row=2, col=1)
            #Update Layouts
            fig.update_layout(margin=dict(t=0))
            fig.update_layout(xaxis_rangeslider_visible=False)
            fig.update_layout(xaxis=dict(
                tickmode='array',
                tickvals=data.index,
                ticktext=data['date']))
            fig.update_xaxes(showgrid=True,row=1,col=1)
            fig.update_xaxes(showgrid=True, row=2, col=1)
            fig.update_yaxes(showgrid=False, row=1, col=1)
            fig.update_yaxes(showgrid=False, row=2, col=1)
            fig.update_traces(showlegend=False)
            fig.update_layout(height=500, width=800,)
            # Show the plot
            #fig.show()
            data=fig.to_image(format='jpg')
            return data
        condition_OP=condition_check(df)
        if str(type(condition_OP))=="<class 'pandas.core.frame.DataFrame'>":
            return Plot_Gen(condition_OP)
    except:
        return None

def RSMA_Extract(ticker,param):
    #print(param)
    try:
        if param[2]=='Weekly':
            df = yf.download(ticker, start=param[3] - datetime.timedelta(days=3000),
                             end=param[3], interval='1wk')

            src = yf.download("^NSEI", start=param[3] - datetime.timedelta(days=3000),
                              end=param[3],interval='1wk')

        elif param[2] == 'Daily':
            src = yf.download("^NSEI", start=param[3] - datetime.timedelta(days=300),
                              end=param[3], interval='1d')
            df = yf.download(ticker, start=param[3]- datetime.timedelta(days=300), end=param[3], interval='1d')

        elif param[2] == 'Hourly':
            src = yf.download("^NSEI", start=param[3] - datetime.timedelta(days=30),
                              end=param[3], interval='1h')
            df = yf.download(ticker, start=param[3]- datetime.timedelta(days=30), end=param[3], interval='1h')
            df = df.reset_index()
            df.rename(columns={'Datetime': 'date'}, inplace=True)
            src = src.reset_index()
            src.rename(columns={'Datetime': 'date'}, inplace=True)


        if param[2]!="Houlry":
            df = df.reset_index()
            df.rename(columns={'Date': 'date'}, inplace=True)
            src = src.reset_index()
            src.rename(columns={'Date': 'date'}, inplace=True)
            df['date'] = df['date'].dt.strftime("%d/%m/%y_%HH")
        df['Ticker'] = ticker
        #quit()
        src = src.iloc[::-1]
        src = src.reset_index(drop=True)
        df = df.iloc[::-1]
        df = df.reset_index(drop=True)
        #-------------------
        #print(df, src)
        df['RS'] = df['Close'] / src['Close']
        df['RS5A'] = df['RS'].rolling(5).mean()
        df['RS5A'] = df['RS5A'].shift(-4)
        df['RS55A'] = df['RS'].rolling(55).mean()
        df['RS55A'] = df['RS55A'].shift(-54)
        df['CMPR'] = df['RS5A']>df['RS55A']
        # print(df.head(10)

        df = df[:-55]
        if df.empty:
            print("In Sufficient Data : ", ticker)
            return None
        #print(df)
        def condition_check(df):
            if (df['CMPR'].head(param[1][0])).all() and \
                    (df['CMPR'][param[1][0]:param[1][0]+param[1][1]]==False).all():
                try:
                    return df.head(param[1][0]+param[1][1]+10)
                except:
                    None
        def Plot_Gen(data):
            fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.05, row_heights=[0.7, 0.3])
            fig.add_trace(go.Candlestick(
                x=data['date'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                increasing_line_color='green', decreasing_line_color='red'), row=1, col=1)

            # Add line plot for close price to the bottom subplot
            fig.add_trace(go.Scatter(x=data['date'], y=data['RS5A'], name='RS5', mode='lines', line=dict(
                color='red', width=2)), row=2, col=1)
            fig.add_trace(go.Scatter(x=data['date'], y=data['RS55A'], name='RS55A', mode='lines', line=dict(
                color='black', width=2)), row=2, col=1)

            # Update Layouts
            fig.update_layout(margin=dict(t=0))
            fig.update_layout(xaxis_rangeslider_visible=False)
            fig.update_layout(xaxis=dict(
                tickmode='array',
                tickvals=data.index,
                ticktext=data['date']))
            fig.update_xaxes(showgrid=True, row=1, col=1)
            fig.update_xaxes(showgrid=True, row=2, col=1)
            fig.update_yaxes(showgrid=False, row=1, col=1)
            fig.update_yaxes(showgrid=False, row=2, col=1)
            fig.update_traces(showlegend=False)
            fig.update_layout(height=500, width=800, )
            fig.update_layout(xaxis_autorange='reversed')
            # fig.show()
            data = fig.to_image(format='jpg')
            return data

        condition_OP=condition_check(df)
        if str(type(condition_OP))=="<class 'pandas.core.frame.DataFrame'>":
            return Plot_Gen(condition_OP)
    except Exception as e:
        print("error",e)
        return None

def RSMALB_Extract(ticker,param):
    #print(param)
    try:
        if param[2]=='Weekly':
            df = yf.download(ticker, start=param[3] - datetime.timedelta(days=3000),
                             end=param[3], interval='1wk')

            src = yf.download("^NSEI", start=param[3] - datetime.timedelta(days=3000),
                              end=param[3],interval='1wk')

        elif param[2] == 'Daily':
            src = yf.download("^NSEI", start=param[3] - datetime.timedelta(days=1000),
                              end=param[3], interval='1d')
            df = yf.download(ticker, start=param[3]- datetime.timedelta(days=1000), end=param[3], interval='1d')

        elif param[2] == 'Hourly':
            src = yf.download("^NSEI", start=param[3] - datetime.timedelta(days=300),
                              end=param[3], interval='1h')
            df = yf.download(ticker, start=param[3]- datetime.timedelta(days=300), end=param[3], interval='1h')
            df = df.reset_index()
            df.rename(columns={'Datetime': 'date'}, inplace=True)
            src = src.reset_index()
            src.rename(columns={'Datetime': 'date'}, inplace=True)
        if param[2]!="Houlry":
            df = df.reset_index()
            df.rename(columns={'Date': 'date'}, inplace=True)
            src = src.reset_index()
            src.rename(columns={'Date': 'date'}, inplace=True)
        df['Ticker'] = ticker

        #-------------------
        df.rename(columns={'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close'},
                  inplace=True)
        lb_df = indicators.LineBreak(df)
        lb_df.line_number = 3
        lb__df = lb_df.get_ohlc_data()
        lb__df = lb__df.drop('index', axis=1)
        lb__df = lb__df.sort_index(ascending=False)
        src.rename(columns={'Date': 'date', 'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close'},
                   inplace=True)
        lb_src = indicators.LineBreak(src)
        lb_src.line_number = 3
        lb__src = lb_src.get_ohlc_data()
        lb__src = lb__src.drop('index', axis=1)
        lb__src = lb__src.sort_index(ascending=False)
        # print(lb__df,lb__src)
        lb__df['RS'] = lb__df['close'] / lb__src['close']
        lb__df['RS5A'] = lb__df['RS'].rolling(5).mean()
        lb__df['RS5A'] = lb__df['RS5A'].shift(-4)
        lb__df['RS55A'] = lb__df['RS'].rolling(55).mean()
        lb__df['RS55A'] = lb__df['RS55A'].shift(-54)
        lb__df['CMPR'] = lb__df['RS5A'] > lb__df['RS55A']
        # print(df.head(10))
        if param[2] == 'Hourly':
            lb__df['date'] = lb__df['date'].dt.strftime("%d/%m/%y_%HH")
        else:
            lb__df['date'] = lb__df['date'].dt.strftime("%d/%m/%y")

        df = lb__df[:-55]
        # print(ticker)
        # print(df.head(20))
        if df.empty:
            print("In Sufficient Data : ", ticker)
            return None
        def condition_check(df):
            if (df['CMPR'].head(param[1][0])).all() and \
                    (df['CMPR'][param[1][0]:param[1][0]+param[1][1]]==False).all():
                try:
                    return df.head(param[1][0]+param[1][1]+20)
                except:
                    None
        def Plot_Gen(data):
            fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.05, row_heights=[0.7, 0.3])
            fig.add_trace(go.Candlestick(
                x=data['date'],
                open=data['open'],
                high=data['high'],
                low=data['low'],
                close=data['close'],
                increasing_line_color='green', decreasing_line_color='red'), row=1, col=1)

            # Add line plot for close price to the bottom subplot
            fig.add_trace(go.Scatter(x=data['date'], y=data['RS5A'], name='RS5', mode='lines', line=dict(
                color='red', width=2)), row=2, col=1)
            fig.add_trace(go.Scatter(x=data['date'], y=data['RS55A'], name='RS55A', mode='lines', line=dict(
                color='black', width=2)), row=2, col=1)

            # Update Layouts
            fig.update_layout(margin=dict(t=0))
            fig.update_layout(xaxis_rangeslider_visible=False)
            fig.update_layout(xaxis=dict(
                tickmode='array',
                tickvals=data.index,
                ticktext=data['date']))
            fig.update_xaxes(showgrid=True, row=1, col=1)
            fig.update_xaxes(showgrid=True, row=2, col=1)
            fig.update_yaxes(showgrid=False, row=1, col=1)
            fig.update_yaxes(showgrid=False, row=2, col=1)
            fig.update_traces(showlegend=False)
            fig.update_layout(height=500, width=850, )
            fig.update_layout(xaxis_autorange='reversed')
            #fig.show()
            data = fig.to_image(format='jpg')
            return data
        condition_OP=condition_check(df)
        if str(type(condition_OP))=="<class 'pandas.core.frame.DataFrame'>":
            return Plot_Gen(condition_OP)
    except Exception as e:
        print("error",e)
        return None

def RSZLLB_Extract(ticker,param):
    #print(param)
    try:
        if param[2]=='Weekly':
            df = yf.download(ticker, start=param[3] - datetime.timedelta(days=3000),
                             end=param[3], interval='1wk')

            src = yf.download("^NSEI", start=param[3] - datetime.timedelta(days=3000),
                              end=param[3],interval='1wk')

        elif param[2] == 'Daily':
            src = yf.download("^NSEI", start=param[3] - datetime.timedelta(days=1000),
                              end=param[3], interval='1d')
            df = yf.download(ticker, start=param[3]- datetime.timedelta(days=1000), end=param[3], interval='1d')
        df = df.reset_index()
        src = src.reset_index()

        df.rename(columns={'Date': 'date', 'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close'},
                  inplace=True)
        lb_df = indicators.LineBreak(df)
        lb_df.line_number = 3
        lb__df = lb_df.get_ohlc_data()
        lb__df = lb__df.drop('index', axis=1)

        src.rename(columns={'Date': 'date', 'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close'},
                   inplace=True)
        lb_src = indicators.LineBreak(src)
        lb_src.line_number = 3
        lb__src = lb_src.get_ohlc_data()
        lb__src = lb__src.drop('index', axis=1)

        lb__df['RS'] = (lb__df['close'].shift(1) / lb__df['close'].shift(param[0])) / (
                lb__src['close'].shift(1) / lb__src['close'].shift(param[0])) - 1
        # print(df.head(10))
        lb__df['date'] = lb__df['date'].dt.strftime("%d/%m/%y")
        #print(lb__df)
        def condition_check(df):
            #if (df['RS'].tail(length) > 0).all():
            if (df['RS'].tail(param[1][0]) > 0).all() and (
                    df['RS'][df.index.argmax() - param[1][0] - param[1][1]:df.index.argmax() - param[1][0]+1] < 0).all():
                try:
                    df = df[df.index.argmax() - param[1][0] - param[1][1]-30:]
                    return df
                except: None
        def Plot_Gen(data):
            fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.05, row_heights=[0.7, 0.3])
            fig.add_trace(go.Candlestick(
                x=data['date'],
                open=data['open'],
                high=data['high'],
                low=data['low'],
                close=data['close'],
                increasing_line_color='green', decreasing_line_color='red'), row=1, col=1)

            PSpan_Data = data[data.index.argmax() - param[1][0] +1 :]
            Trans_Data = data[data.index.argmax() - param[1][0] : data.index.argmax() - param[1][0] +2]
            NSpan_Data = data[data.index.argmax() - param[1][0] - param[1][1] : data.index.argmax() - param[1][0]+1]
            Cushion_Data = data[data.index.argmax() - param[1][0] - param[1][1]-30: \
                                data.index.argmax() - param[1][0] - param[1][1]+1]

            # Add line plot for close price to the bottom subplot
            fig.add_trace(go.Scatter(x=NSpan_Data['date'], y=NSpan_Data['RS'], name='NRS', mode='lines', line= dict(
                color='red',width=2)), row=2, col=1)
            fig.add_trace(go.Scatter(x=PSpan_Data['date'], y=PSpan_Data['RS'], name='PRS', mode='lines', line= dict(
                color='Green',width=2)), row=2, col=1)
            fig.add_trace(go.Scatter(x=Trans_Data['date'], y=Trans_Data['RS'], name='TRNRS', mode='lines+markers',
                                     line= dict(color='#00008B',width=2)), row=2, col=1)
            fig.add_trace(go.Scatter(x=Cushion_Data['date'], y=Cushion_Data['RS'], name='NRS', mode='lines', line= dict(
                color='Black',width=2)), row=2, col=1)
            #Update Layouts
            fig.update_layout(margin=dict(t=0))
            fig.update_layout(xaxis_rangeslider_visible=False)
            fig.update_layout(xaxis=dict(
                tickmode='array',
                tickvals=data.index,
                ticktext=data['date']))
            fig.update_xaxes(showgrid=True,row=1,col=1)
            fig.update_xaxes(showgrid=True, row=2, col=1)
            fig.update_yaxes(showgrid=False, row=1, col=1)
            fig.update_yaxes(showgrid=False, row=2, col=1)
            fig.update_traces(showlegend=False)
            fig.update_layout(height=500, width=800,)
            # Show the plot
            #fig.show()
            data=fig.to_image(format='jpg')
            return data
        condition_OP=condition_check(lb__df)
        if str(type(condition_OP))=="<class 'pandas.core.frame.DataFrame'>":
            return Plot_Gen(condition_OP)
    except Exception as e:
        print("error",e)
        return None
@st.cache_data
def getlist(a,param):
    progress = st.progress(0, text="WIP")
    if a == "Nifty50":
        path="Directory/NSE50.csv"
    elif a == "FnO":
        path="Directory/FNO.csv"
    elif a == "BSE ALL":
        path="Directory/ALLBSE.csv"
    elif a == "BSE250 Small Cap":
        path="Directory/BSE_250_SMALLCAP.csv"
    elif a == "BSE400 Mid Small Cap":
        path="Directory/BSE_400_MIDSMALL.csv"
    elif a == "BSE250 LargeMid":
        path="Directory/BSE_250_LARGEMID.csv"


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
    #print("X",script_list)
    i=0
    j=1
    for item2 in script_list:
        cur=script_list.index(item2)
        sumlen=len(script_list)
        progress.progress(int(round(cur/sumlen*100,0)),text="%d of %d Processed"%(cur,sumlen))
        op=RSZL_Extract(item2,param)

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
@st.cache_data
def getlist_T2(a,param):
    progress = st.progress(0, text="WIP")
    if a == "Nifty50":
        path="Directory/NSE50.csv"
    elif a == "FnO":
        path="Directory/FNO.csv"
    elif a == "BSE ALL":
        path="Directory/ALLBSE.csv"
    elif a == "BSE250 Small Cap":
        path="Directory/BSE_250_SMALLCAP.csv"
    elif a == "BSE400 Mid Small Cap":
        path="Directory/BSE_400_MIDSMALL.csv"
    elif a == "BSE250 LargeMid":
        path="Directory/BSE_250_LARGEMID.csv"


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
    #print("X",script_list)
    i=0
    j=1
    for item2 in script_list:
        cur=script_list.index(item2)
        sumlen=len(script_list)
        progress.progress(int(round(cur/sumlen*100,0)),text="%d of %d Processed"%(cur,sumlen))
        op=RSMA_Extract(item2,param)

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
@st.cache_data
def getlist_T3(a,param):
    progress = st.progress(0, text="WIP")
    if a == "Nifty50":
        path="Directory/NSE50.csv"
    elif a == "FnO":
        path="Directory/FNO.csv"
    elif a == "BSE ALL":
        path="Directory/ALLBSE.csv"
    elif a == "BSE250 Small Cap":
        path="Directory/BSE_250_SMALLCAP.csv"
    elif a == "BSE400 Mid Small Cap":
        path="Directory/BSE_400_MIDSMALL.csv"
    elif a == "BSE250 LargeMid":
        path="Directory/BSE_250_LARGEMID.csv"

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
    #print("X",script_list)
    i=0
    j=1
    for item2 in script_list:
        cur=script_list.index(item2)
        sumlen=len(script_list)
        progress.progress(int(round(cur/sumlen*100,0)),text="%d of %d Processed"%(cur,sumlen))
        op=RSMALB_Extract(item2,param)

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
@st.cache_data
def getlist_T4(a,param):
    progress = st.progress(0, text="WIP")
    if a == "Nifty50":
        path="Directory/NSE50.csv"
    elif a == "FnO":
        path="Directory/FNO.csv"
    elif a == "BSE ALL":
        path="Directory/ALLBSE.csv"
    elif a == "BSE250 Small Cap":
        path="Directory/BSE_250_SMALLCAP.csv"
    elif a == "BSE400 Mid Small Cap":
        path="Directory/BSE_400_MIDSMALL.csv"
    elif a == "BSE250 LargeMid":
        path="Directory/BSE_250_LARGEMID.csv"

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
    i=0
    j=1
    for item2 in script_list:
        cur=script_list.index(item2)
        sumlen=len(script_list)
        progress.progress(int(round(cur/sumlen*100,0)),text="%d of %d Processed"%(cur,sumlen))
        op=RSZLLB_Extract(item2,param)

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

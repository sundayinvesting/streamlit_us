import datetime
import os
import pandas as pd
import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
import requests
from io import StringIO
from stocktrends import indicators

direc=r'C:\Users\Dell\Desktop\Temp'

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
        print(df.tail(10))
        df.rename(columns={'Date': 'date'}, inplace=True)
        src = src.reset_index()
        src.rename(columns={'Date': 'date'}, inplace=True)
        df['date'] = df['date'].dt.strftime("%d/%m/%y_%HH")
        df['Ticker'] = ticker
        #print(src.tail(10))
        df['RS']=round(((df['Close'].shift(1)/df['Close'].shift(param[0]))/(
                                src['Close'].shift(1)/src['Close'].shift(param[0]))-1),3)
        df.to_csv(r'C:\Users\Dell\Desktop\Temp\data.csv')
        #print(df,src)
        def condition_check(df):
            #if (df['RS'].tail(length) > 0).all():
            if (df['RS'].tail(param[1][0]) > 0).all() and (
                    df['RS'][df.index.argmax() - param[1][0] - param[1][1]:df.index.argmax() - param[1][0]+1] < 0).all():
                try:
                    df = df[df.index.argmax() - param[1][0] - param[1][1]-5:]
                    return df
                except:
                    df = df[df.index.argmax() - param[1][0] - param[1][1]-5:]
                    return df
            else:
                df = df[df.index.argmax() - param[1][0] - param[1][1] - 5:]
                return df

        def Plot_Gen(data):
            fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.05, row_heights=[0.7, 0.3])
            fig.add_trace(go.Candlestick(
                x=data['date'],
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                increasing_line_color='green', decreasing_line_color='red'), row=1, col=1)
            #fig.update_layout(title=ticker)
            PSpan_Data = data[data.index.argmax() - param[1][0] +1 :]
            Trans_Data = data[data.index.argmax() - param[1][0] : data.index.argmax() - param[1][0] +2]
            NSpan_Data = data[data.index.argmax() - param[1][0] - param[1][1] : data.index.argmax() - param[1][0]+1]
            Cushion_Data = data[data.index.argmax() - param[1][0] - param[1][1]-5: \
                                data.index.argmax() - param[1][0] - param[1][1]+1]

            # Add line plot for close price to the bottom subplot
            fig.add_trace(go.Scatter(x=NSpan_Data['date'], y=NSpan_Data['RS'], name='NRS', mode='lines', line= dict(
                width=2)), row=2, col=1)
            fig.add_trace(go.Scatter(x=PSpan_Data['date'], y=PSpan_Data['RS'], name='PRS', mode='lines', line= dict(
                width=2)), row=2, col=1)
            fig.add_trace(go.Scatter(x=Trans_Data['date'], y=Trans_Data['RS'], name='TRNRS', mode='lines',
                                     line= dict(width=2)), row=2, col=1)
            fig.add_trace(go.Scatter(x=Cushion_Data['date'], y=Cushion_Data['RS'], name='NRS', mode='lines', line= dict(
                width=2)), row=2, col=1)
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
            fig.write_image(direc+f'\\{ticker+"_RSZL"}.jpg')
            os.system(direc+f'\\{ticker+"_RSZL"}.jpg')
            data=fig.to_image(format='jpg')
            return data
        condition_OP=condition_check(df)
        if str(type(condition_OP))=="<class 'pandas.core.frame.DataFrame'>":
            return Plot_Gen(condition_OP)
    except Exception as e:
        print(e)

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
        print(df.tail(10))
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
            else: return df.head(param[1][0]+param[1][1]+10)
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
            fig.update_layout(title='My Graph')
            fig.write_image(direc+f'\\{ticker+"_RSZL"}.jpg')
            os.system(direc+f'\\{ticker+"_RSZL"}.jpg')
            # fig.show()
            data = fig.to_image(format='jpg')
            return data

        condition_OP=condition_check(df)
        if str(type(condition_OP))=="<class 'pandas.core.frame.DataFrame'>":
            return Plot_Gen(condition_OP)
    except Exception as e:
        print("error",e)
        return None

RSZL_Extract("ADANIENT.NS",[55,[10,10],"Daily",datetime.datetime.today()-datetime.timedelta(0),"NSE500"])
#RSMA_Extract("ABBOTINDIA.BO",[55,[30,1],"Daily",datetime.datetime.today()-datetime.timedelta(0)])
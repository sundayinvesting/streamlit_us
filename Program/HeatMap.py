import datetime
import time
import pandas as pd
import pandas_ta as ta
import streamlit as st
import yfinance as yf
from datetime import datetime as dt
import requests
from io import StringIO

token = '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'
owner = 'sundayinvesting'
repo = 'Streamlit'

r = requests.get(
    'https://api.github.com/repos/{owner}/{repo}/contents/{path}'.format(
        owner=owner, repo=repo, path="Directory/NSE50.csv"),
    headers={
        'accept': 'application/vnd.github.v3.raw',
        'authorization': 'token {}'.format(token)
    })
string_io_obj = StringIO(r.text)
stocklist_NS50 = pd.read_csv(string_io_obj, sep=",", index_col=0, header=None).reset_index()[0].values.tolist()
#--
r = requests.get(
    'https://api.github.com/repos/{owner}/{repo}/contents/{path}'.format(
        owner=owner, repo=repo, path="Directory/NSE500.csv"),
    headers={
        'accept': 'application/vnd.github.v3.raw',
        'authorization': 'token {}'.format(token)
    })
string_io_obj = StringIO(r.text)
stocklist_NS500 = pd.read_csv(string_io_obj, sep=",", index_col=0, header=None).reset_index()[0].values.tolist()
#--
r = requests.get(
    'https://api.github.com/repos/{owner}/{repo}/contents/{path}'.format(
        owner=owner, repo=repo, path="Directory/FNO.csv"),
    headers={
        'accept': 'application/vnd.github.v3.raw',
        'authorization': 'token {}'.format(token)
    })
string_io_obj = StringIO(r.text)
stocklist_FNO = pd.read_csv(string_io_obj, sep=",", index_col=0, header=None).reset_index()[0].values.tolist()
#print(len(stocklist_FNO))
issuelist=[]
@st.cache_data
def DataPull(start,tframe):
    progress = st.progress(0, text="WIP")
    length=20
    opdata = []
    sumlen=len(stocklist_FNO)+len(stocklist_NS50)+len(stocklist_NS500)
    cur=0
    for stocklist in [stocklist_NS50,stocklist_NS500,stocklist_FNO]:
        #print(start)
        if tframe == "Daily":
            data = yf.download(stocklist[0], start - datetime.timedelta(length*20),start).reset_index()
        else:
            data = yf.download(stocklist[0], start - datetime.timedelta(length * 200),start,interval='1wk').reset_index()

        #print(stocklist,data)

        rsi50_data = data[['Date']].tail(length).reset_index(drop=True)
        rsi60_data = data[['Date']].tail(length).reset_index(drop=True)
        ema20_data = data[['Date']].tail(length).reset_index(drop=True)
        ema50_data = data[['Date']].tail(length).reset_index(drop=True)
        ema100_data = data[['Date']].tail(length).reset_index(drop=True)
        ema200_data = data[['Date']].tail(length).reset_index(drop=True)
        spr_trend = data[['Date']].tail(length).reset_index(drop=True)
        rs1 = data[['Date']].tail(length).reset_index(drop=True)
        if tframe == "Daily":
            src = yf.download("^NSEI", start - datetime.timedelta(length*20), start).reset_index()
        else:
            src = yf.download("^NSEI", start - datetime.timedelta(length * 200),start,interval='1wk').reset_index()

        #stocklist=[stocklist[0]]
        for step in stocklist:
            cur+=1
            if cur<50:
                progress.progress(int(round(cur / sumlen * 100, 0)),"Processing : Nifty 50 ")
            elif cur>550:
                progress.progress(int(round(cur / sumlen * 100, 0)),"Processing : Nifty 500 ")
            else:
                progress.progress(int(round(cur / sumlen * 100, 0)), "Processing : FnO ")
            try:
                print(step)
                try:
                    if tframe == "Daily":
                        data = yf.download(step, start - datetime.timedelta(length * 20), start).reset_index()
                    else:
                        data = yf.download(step, start - datetime.timedelta(length * 200), start,
                                           interval='1wk').reset_index()
                except Exception as e: print(e);pass
                close=data['Close'].tail(length).reset_index()
                # rsi extraction
                rsi_data = pd.DataFrame({step:ta.momentum.rsi(data['Close'], window=14).tolist()[-length:]})
                rsi50_data=pd.concat([rsi50_data,rsi_data],axis=1)
                rsi50_data[step] = rsi50_data[step].apply(lambda x: True if x > 50 else False)
                rsi60_data=pd.concat([rsi60_data,rsi_data],axis=1)
                rsi60_data[step] = rsi60_data[step].apply(lambda x: True if x > 60 else False)
                # # ema extraction

                ema20_data = pd.concat([ema20_data, pd.DataFrame({step: ta.overlap.ema(data["Close"],
                                                                                length=20).tolist()[-length:]})], axis=1)
                ema20_data[step] = ema20_data[step]<close['Close']
                #---
                ema50_data = pd.concat([ema50_data, pd.DataFrame({step: ta.overlap.ema(data["Close"],
                                                                                length=50).tolist()[-length:]})], axis=1)
                ema50_data[step] = ema50_data[step]<close['Close']
                # ---
                ema100_data = pd.concat([ema100_data, pd.DataFrame({step: ta.overlap.ema(data["Close"],
                                                                                length=100).tolist()[-length:]})], axis=1)
                ema100_data[step] = ema100_data[step]<close['Close']
                # ---
                ema200_data = pd.concat([ema200_data, pd.DataFrame({step: ta.overlap.ema(data["Close"],
                                                                                length=200).tolist()[-length:]})], axis=1)
                ema200_data[step] = ema200_data[step]<close['Close']
                #---
                spr_trend = pd.concat([spr_trend, pd.DataFrame({step: ta.overlap.supertrend(data['High'],
                    data['Low'], data['Close'], multiplier=3,length=10)['SUPERT_10_3.0'].tolist()[-length:]})],axis=1)
                spr_trend[step] = spr_trend[step]<close['Close']

                # RS1 Calculation
                rs1 = pd.concat([rs1, pd.DataFrame({step: ((data['Close'].shift(1)/data['Close'].shift(55))/(
                        src['Close'].shift(1)/src['Close'].shift(55))-1).tolist()[-length:]})],axis=1)
                rs1[step] = rs1[step]>0
            except Exception as e:
                issuelist.append(step)

                #stocklist.remove(step)
                print(e);pass
        #quit()
        #ema20_data.to_csv(r"C:\Users\DELL\Desktop\ema.csv")
        #ema200_data.to_csv(r"C:\Users\DELL\Desktop\ema12.csv")

        rsi50_data['rsi pivot'] = rsi50_data[rsi50_data.columns.tolist()[1:]].sum(axis=1).apply(lambda x : int(round((x/len(
            rsi50_data.columns.tolist()[1:]))*100,0)))
        rsi60_data['rsi pivot'] = rsi60_data[rsi60_data.columns.tolist()[1:]].sum(axis=1).apply(lambda x : int(round((x/len(rsi60_data.columns.tolist()[1:]))*100,0)))
        ema20_data['ema pivot'] = ema20_data[ema20_data.columns.tolist()[1:]].sum(axis=1).apply(lambda x : int(round((x/len(ema20_data.columns.tolist()[1:]))*100,0)))
        ema50_data['ema pivot'] = ema50_data[ema50_data.columns.tolist()[1:]].sum(axis=1).apply(lambda x : int(round(
            (x/len(ema50_data.columns.tolist()[1:]))*100,0)))
        ema100_data['ema pivot'] = ema100_data[ema100_data.columns.tolist()[1:]].sum(axis=1).apply(lambda x : int(
            round((x/len(ema100_data.columns.tolist()[1:]))*100,0)))
        ema200_data['ema pivot'] = ema200_data[ema200_data.columns.tolist()[1:]].sum(axis=1).apply(lambda x : int(
            round((x/len(ema200_data.columns.tolist()[1:]))*100,0)))
        spr_trend['spr_pivot'] = spr_trend[spr_trend.columns.tolist()[1:]].sum(axis=1).apply(lambda x : int(round((x/len(spr_trend.columns.tolist()[1:]))*100,0)))
        rs1['pivot'] = rs1[rs1.columns.tolist()[1:]].sum(axis=1).apply(lambda x : int(round((x/len(rs1.columns.tolist()[1:]))*100,0)))
        # print(rs1['pivot'])
        Output = pd.DataFrame({
            "Date": rsi50_data['Date'],
            "Diff.": src['Close'].diff()[-length:].tolist(),
            "RS55>0": rs1['pivot'],
            "RSI>50": rsi50_data['rsi pivot'],
            "RSI>60": rsi60_data['rsi pivot'],
            "EMA20": ema20_data['ema pivot'],
            "EMA50": ema50_data['ema pivot'],
            "EMA100": ema100_data['ema pivot'],
            "EMA200": ema200_data['ema pivot'],
            "Super Trend": spr_trend['spr_pivot']
        }).reset_index(drop=True).sort_values(by='Date')
        Output['Diff.']=Output['Diff.'].round(1).astype(str)
        Output.to_csv(r'C:\Users\DELL\Desktop\Temp\HeatMap.csv')
        Output['Date'] = Output['Date'].dt.date
        Output = Output.iloc[::-1]
        print(Output)
        opdata.append(Output)
        print(issuelist)
    progress.progress(100, "Extracted")
    opdata.append(src['Close'].tail(1).tolist()[0])
    #print(Output)

    return opdata

#DataPull()
#DataPull(datetime.datetime.strptime("2023-05-01","%Y-%m-%d"),"Weekly")
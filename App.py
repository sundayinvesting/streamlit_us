# Streamlit Test File
import streamlit as st
st.set_page_config(layout="wide")
from Program import Bullish_trendline
from Program import Bearish_trendline
from Program import Triangle_Trendline
from Program import Promoter_Strategy
from Program import Promoter_Data
from Program import RS_Extract
import datetime
from Program import HeatMap

def cond_format(val):
    try:
        if val >= 85:
            color = "#4BEC00"
        elif val >= 80:
            color = "#9EF411"
        elif val >= 70:
            color = "#CEF411"
        elif val >= 60:
            color = "#F4F111"
        elif val >= 50:
            color = "#ECB600"
        elif val >= 30:
            color = "#EC8400"
        elif val >= 20:
            color = "#EC4B00"
        elif val >= 0:
            color = "#EC2000"
        else:
            color = 'white'
    except:
        color = 'white'

    return f'background-color: {color}'

def font_color(val):
    if val != None: color = "black"
    return f'color: {color}'

st.title('Investing USA:first_place_medal:')
tab_widget=st.tabs(["Trendline Strategy","Promoter Buy Strategy","Market Heat Map",
                    "Relative Strength Strategy"])

# with tab_widget[0]:
#     col_w1, col_w2 = st.columns(2, gap='small')
#     col_w3, col_w4 = st.columns(2, gap='small')
#     col_w5, col_w6 = st.columns(2, gap='small')
#     USDINR='''
# <!-- TradingView Widget BEGIN -->
# <div class="tradingview-widget-container">
#   <div id="tradingview_cddd0"></div>
#   <div class="tradingview-widget-copyright"><a href="https://in.tradingview.com/symbols/USDINR/?exchange=FX_IDC" rel="noopener" target="_blank"><span class="blue-text">USD INR chart</span></a> by TradingView</div>
#   <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
#   <script type="text/javascript">
#   new TradingView.widget(
#   {
#   "width": 650,
#   "height": 500,
#   "symbol": "FX_IDC:USDINR",
#   "interval": "D",
#   "timezone": "Etc/UTC",
#   "allow_symbol_change": true,
#   "theme": "dark",
#   "style": "1",
#   "locale": "in",
#   "toolbar_bg": "#f1f3f6",
#   "enable_publishing": false,
#   "save_image": false,
#   "studies": [
#     "STD;RSI",
#     "STD;SMA"
#   ],
#   "container_id": "tradingview_cddd0"
# }
#   );
#   // Add EMA20 indicator
#   var widget = window.tvWidget && window.tvWidget.activeChart();
#   if (widget) {
#     widget.chart().createStudy("EMA", false, false, [20], null, {"plot.color.0": "#FFA500"});
#   }
#   </script>
# </div>
# <!-- TradingView Widget END -->'''
#     Gold="""
# <!-- TradingView Widget BEGIN -->
# <div class="tradingview-widget-container">
#   <div id="tradingview_c3664"></div>
#   <div class="tradingview-widget-copyright"><a href="https://in.tradingview.com/symbols/XAUINR/?exchange=FX_IDC" rel="noopener" target="_blank"><span class="blue-text">XAUINR chart</span></a> by TradingView</div>
#   <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
#   <script type="text/javascript">
#   new TradingView.widget(
#   {
#   "width": 650,
#   "height": 500,
#   "symbol": "FX_IDC:XAUINR",
#   "interval": "D",
#   "timezone": "Etc/UTC",
#   "theme": "dark",
#   "style": "1",
#   "locale": "in",
#   "toolbar_bg": "#f1f3f6",
#   "enable_publishing": false,
#   "allow_symbol_change": true,
#   "save_image": false,
#   "studies": [
#     "STD;RSI",
#     "STD;SMA"
#   ],
#   "container_id": "tradingview_c3664"
# }
#   );
#   </script>
# </div>
# <!-- TradingView Widget END -->
# """
#     NASDAQ="""
#     <!-- TradingView Widget BEGIN -->
# <div class="tradingview-widget-container">
#   <div id="tradingview_19dcb"></div>
#   <div class="tradingview-widget-copyright"><a href="https://in.tradingview.com/symbols/NASDAQ-NDX/" rel="noopener" target="_blank"><span class="blue-text">NDX chart</span></a> by TradingView</div>
#   <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
#   <script type="text/javascript">
#   new TradingView.widget(
#   {
#   "width": 650,
#   "height": 500,
#   "symbol": "NASDAQ:NDX",
#   "interval": "D",
#   "timezone": "Etc/UTC",
#   "theme": "dark",
#   "style": "1",
#   "locale": "in",
#   "toolbar_bg": "#f1f3f6",
#   "enable_publishing": false,
#   "allow_symbol_change": true,
#   "save_image": false,
#   "studies": [
#     "STD;RSI",
#     "STD;SMA"
#   ],
#   "container_id": "tradingview_19dcb"
# }
#   );
#   </script>
# </div>
# <!-- TradingView Widget END -->
#     """
#     Crude="""
# <!-- TradingView Widget BEGIN -->
# <div class="tradingview-widget-container">
#   <div id="tradingview_7e673"></div>
#   <div class="tradingview-widget-copyright"><a href="https://in.tradingview.com/symbols/OIL_CRUDE/?exchange=CURRENCYCOM" rel="noopener" target="_blank"><span class="blue-text">OIL_CRUDE chart</span></a> by TradingView</div>
#   <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
#   <script type="text/javascript">
#   new TradingView.widget(
#   {
#   "width": 650,
#   "height": 500,
#   "symbol": "CURRENCYCOM:OIL_CRUDE",
#   "interval": "D",
#   "timezone": "Etc/UTC",
#   "theme": "dark",
#   "style": "1",
#   "locale": "in",
#   "toolbar_bg": "#f1f3f6",
#   "enable_publishing": false,
#   "allow_symbol_change": true,
#   "save_image": false,
#   "studies": [
#     "STD;RSI",
#     "STD;SMA"
#   ],
#   "container_id": "tradingview_7e673"
# }
#   );
#   </script>
# </div>
# <!-- TradingView Widget END -->
#     """
#     with col_w1:
#         st.components.v1.html(NASDAQ,width=650,height=480)
#     with col_w2:
#         st.components.v1.html(Crude,width=650,height=480)
#     with col_w3:
#         st.components.v1.html(USDINR,width=650,height=480)
#     with col_w4:
#         st.components.v1.html(Gold,width=650,height=480)

with tab_widget[0]:
    tab_widget_tl = st.tabs(["Bullish","Bearish","Asc. Triangle"])
    with tab_widget_tl[0]:
        st.header('Bullish Trendline Graph Generation')
        col_w1,col_w2,col_w3 = st.columns(3,gap='medium')
        with col_w1:
            index = st.selectbox("Index", options=["Nifty50", "FnO"],)
        with col_w3:
            time_frame = st.selectbox(label='Time Frame', options=('Weekly','Daily','Hourly'))
        with col_w2:
            gen_date_S1 = st.date_input(label="Start Date",)
            gen_date = datetime.datetime.strptime(datetime.datetime.strftime(gen_date_S1,"%Y-%m-%d"),"%Y-%m-%d")
            print(gen_date)
        col_w4, col_w5 = st.columns(2,gap='large')
        with col_w4:
            accuracy = st.slider(label=' % Accuracy', min_value=1, max_value=10, step=1, value=5)
        with col_w5:
            mountain_peak=st.slider(label='Mountain Peak',min_value=5,max_value=50,step=5,value=25)
        if st.button('Generate',use_container_width=True):
            Bullish_trendline.fun_getlist(index,[time_frame,accuracy/100,mountain_peak,gen_date])

    with tab_widget_tl[1]:
        st.header('Bearish Trendline Graph Generation')
        col_w1, col_w2,col_w3 = st.columns(3,gap='medium')
        with col_w1:
            index = st.selectbox("Index", options=["Nifty50", "FnO"],key='BRS1')
        with col_w3:
            time_frame = st.selectbox(label='Time Frame', options=('Weekly','Daily','Hourly'),key='BRS2')
        with col_w2:
            gen_date_S1 = st.date_input(label="Start Date",key='BRS3')
            gen_date = datetime.datetime.strptime(datetime.datetime.strftime(gen_date_S1,"%Y-%m-%d"),"%Y-%m-%d")
            print(gen_date)
        col_w4, col_w5 = st.columns(2,gap='large')
        with col_w4:
            accuracy = st.slider(label=' % Accuracy', min_value=1, max_value=10, step=1, value=5,key='BRS4')
        with col_w5:
            mountain_peak=st.slider(label='Mountain Peak',min_value=5,max_value=50,step=5,value=25,key='BRS5')
        if st.button('Generate',use_container_width=True,key='BRS6'):
            Bearish_trendline.fun_getlist(index,[time_frame,accuracy/100,mountain_peak,gen_date])

    with tab_widget_tl[2]:
        st.header('Triangular Trendline Graph Generation')
        col_w1, col_w2, col_w3 = st.columns(3, gap='medium')
        with col_w1:
            index = st.selectbox("Index", options=["Nifty50","NIFTY500", "FnO",], key='TRS1')
        with col_w3:
            time_frame = st.selectbox(label='Time Frame', options=('Weekly', 'Daily', 'Hourly'), key='TRS2')
        with col_w2:
            gen_date_S1 = st.date_input(label="Start Date", key='TRS3')
            gen_date = datetime.datetime.strptime(datetime.datetime.strftime(gen_date_S1, "%Y-%m-%d"), "%Y-%m-%d")
        mountain_peak = st.slider(label='Mountain Peak', min_value=3, max_value=15, step=2, value=7,
                                      key='TRS5')
        if st.button('Generate', use_container_width=True, key='TRS6'):
            Triangle_Trendline.fun_getlist(index, [time_frame, mountain_peak, gen_date])

with tab_widget[1]:
    st.title("Promoter Buy/Sell")
    col1,col2=st.columns(2)
    with col1:
        start=st.date_input(label="Start Date",value=datetime.datetime.today()-datetime.timedelta(90))
    with col2:
        end=st.date_input(label="End Date",value=datetime.datetime.today())
    if st.button("Pull Data",use_container_width=True,):
        with st.spinner("Extracting"):
            gen_op=Promoter_Data.data_push(start.strftime("%d-%m-%Y"), end.strftime("%d-%m-%Y"))
            st.text("Values in Cr. Rs")
            left_co1, cent_co1, last_co1 = st.columns([1,3,1])
            with cent_co1:
                if gen_op[1][0] !=None:
                    st.image(gen_op[1][0][0])
            left_co, cent_co, last_co = st.columns([1,3,1])
            with cent_co:
                if gen_op[1][1] != None:
                    st.image(gen_op[1][1][0])
            left_co1, cent_co1, last_co1 = st.columns([1,3,1])
            with cent_co1:
                if gen_op[1][2] != None:
                    st.image(gen_op[1][2][0])
            left_co1, cent_co1, last_co1 = st.columns([1,3,1])
            with cent_co1:
                if gen_op[1][3] != None:
                    st.image(gen_op[1][3][0])
            st.dataframe(gen_op[0], use_container_width=True)

with tab_widget[2]:
    heading_style = """
        <style>
        th {
            background-color: blue;
            color: white;
            font-weight: bold;
            text-align: center;
        }
        </style>
    """
    col_w1, col_w2, = st.columns(2, gap='medium')
    with col_w1:
        HeatMap_startDate = st.date_input(label="Date Range",key='HeatMapStart')
        #HeatMap_startDate = datetime.datetime.strptime(datetime.datetime.strftime(gen_date_S1,"%Y-%m-%d"),"%Y-%m-%d")
    with col_w2:
        HeatMap_timeframe = st.selectbox(label='Time Frame', options=('Daily','Weekly'))
    if st.button('Extract',use_container_width=True):

        st.text("Values in %")
        Output=HeatMap.DataPull(HeatMap_startDate,HeatMap_timeframe)
        Output0 =Output[0].style.set_properties(**{'color': 'black', 'background-color': 'white'}). \
                applymap(cond_format,
                         subset=['RS55>0',
                                 'RSI>50',
                                 'RSI>60',
                                 'EMA20',
                                 'EMA50',
                                 "EMA100",
                                 'EMA200',
                                 "Super Trend"]). \
                hide(axis='index')
        left_co1, cent_co1, last_co1 = st.columns([1, 3, 1])
        with cent_co1:
            st.write(" \n\n ")
            st.write(f"NSE50 Overview : Close Value {Output[3]}")
            #st.dataframe(Output0,use_container_width=True)
            st.write(heading_style, unsafe_allow_html=True)
            st.write(Output0.to_html(index=False, escape=False), unsafe_allow_html=True)
        Output1 = Output[1].style.set_properties(**{'color': 'black', 'background-color': 'white'}). \
                applymap(cond_format,
                         subset=['RS55>0',
                                 'RSI>50',
                                 'RSI>60',
                                 'EMA20',
                                 'EMA50',
                                 "EMA100",
                                 'EMA200',
                                 "Super Trend"]). \
                hide(axis='index')

        left_co1, cent_co1, last_co1 = st.columns([1, 3, 1])
        with cent_co1:
            st.write(" \n\n ")
            st.write(f"NSE500 Overview  : Close Value {Output[3]}")
            #st.dataframe(Output1,use_container_width=True)
            st.write(heading_style, unsafe_allow_html=True)
            st.write(Output1.to_html(index=False, escape=False), unsafe_allow_html=True)

        Output2 = Output[2].style.set_properties(**{'color': 'black', 'background-color': 'white'}). \
                applymap(cond_format,
                         subset=['RS55>0',
                                 'RSI>50',
                                 'RSI>60',
                                 'EMA20',
                                 'EMA50',
                                 "EMA100",
                                 'EMA200',
                                 "Super Trend"]). \
                hide(axis='index')

        left_co1, cent_co1, last_co1 = st.columns([1, 3, 1])
        with cent_co1:
            st.write(" \n\n ")
            st.write(f"FnO Overview  : Close Value {Output[3]}")
            #st.dataframe(Output2,use_container_width=True)
            st.write(heading_style, unsafe_allow_html=True)
            st.write(Output2.to_html(index=False, escape=False), unsafe_allow_html=True)

with tab_widget[3]:
    tab_widget_t2 = st.tabs(["Zero Line : Candle Stick", "Moving Average : Candlestick",
                             "Zero Line : Line Break", "Moving Average : LineBreak"])
    with tab_widget_t2[0]:
        col_w1, col_w2, col_w2a = st.columns(3, gap='medium')
        with col_w1:
            index = st.selectbox("Index", options=["Nifty50", "FnO", "BSE250 LargeMid" ,
                                                   "BSE250 Small Cap", "BSE400 Mid Small Cap", "BSE ALL",],
                                 key='RS1')
        with col_w2:
            time_frame = st.selectbox(label='Time Frame', options=('Daily','Weekly',),key='RS2')
        with col_w2a:
            daterange = st.date_input(label="Date Range",key='RSZL_Start')

        col_w3, col_w4, col_w5 = st.columns(3, gap='medium')
        with col_w3:
            RS_Shift = st.slider(label='RS Shift', min_value=10, max_value=125, step=5, value=55,key='RS3')
        with col_w4:
            nSpan = st.slider(label='-ve Span', min_value=1, max_value=60, step=1, value=5,key='RS4')
        with col_w5:
            pSpan = st.slider(label='+ve Span', min_value=1, max_value=60, step=1, value=5,key='RS5')
        if st.button('Generate', use_container_width=True,key='RS6'):
            RS_Extract.getlist(index,[RS_Shift,[pSpan,nSpan],time_frame,daterange])
    with tab_widget_t2[1]:
        col_w1, col_w2, col_w2a = st.columns(3, gap='medium')
        with col_w1:
            index = st.selectbox("Index", options=["Nifty50", "FnO", "BSE250 LargeMid",
                                                   "BSE250 Small Cap", "BSE400 Mid Small Cap", "BSE ALL", ],
                                 key='RSma1')
        with col_w2:
            time_frame = st.selectbox(label='Time Frame', options=('Daily', 'Weekly','Hourly'), key='RSma2')
        with col_w2a:
            daterange = st.date_input(label="Date Range", key='RSma_Start')

        col_w4, col_w5 = st.columns(2, gap='medium')
        with col_w4:
            nSpan = st.slider(label='-ve Span', min_value=1, max_value=60, step=1, value=5, key='RSma4')
        with col_w5:
            pSpan = st.slider(label='+ve Span', min_value=1, max_value=60, step=1, value=5, key='RSma5')
        if st.button('Generate', use_container_width=True, key='RSma6'):
            RS_Extract.getlist_T2(index, [None, [pSpan, nSpan], time_frame, daterange])
    with tab_widget_t2[2]:
        col_w1, col_w2, col_w2a = st.columns(3, gap='medium')
        with col_w1:
            index = st.selectbox("Index", options=["Nifty50", "FnO", "BSE250 LargeMid" ,
                                                   "BSE250 Small Cap", "BSE400 Mid Small Cap", "BSE ALL",],
                                 key='RS1lb')
        with col_w2:
            time_frame = st.selectbox(label='Time Frame', options=('Daily','Weekly',),key='RS2lb')
        with col_w2a:
            daterange = st.date_input(label="Date Range",key='RSZLlb_Start')
        col_w3, col_w4, col_w5 = st.columns(3, gap='medium')
        with col_w3:
            RS_Shift = st.slider(label='RS Shift', min_value=10, max_value=125, step=5, value=55,key='RS3lb')
        with col_w4:
            nSpan = st.slider(label='-ve Span', min_value=1, max_value=60, step=1, value=5,key='RS4lb')
        with col_w5:
            pSpan = st.slider(label='+ve Span', min_value=1, max_value=60, step=1, value=5,key='RS5lb')
        if st.button('Generate', use_container_width=True,key='RS6lb'):
            RS_Extract.getlist_T4(index,[RS_Shift,[pSpan,nSpan],time_frame,daterange])
    with tab_widget_t2[3]:
        col_w1, col_w2, col_w2a = st.columns(3, gap='medium')
        with col_w1:
            index = st.selectbox("Index", options=["Nifty50", "FnO", "BSE250 LargeMid",
                                                   "BSE250 Small Cap", "BSE400 Mid Small Cap", "BSE ALL", ],
                                 key='RSmalb1')
        with col_w2:
            time_frame = st.selectbox(label='Time Frame', options=('Daily', 'Weekly','Hourly'), key='RSmalb2')
        with col_w2a:
            daterange = st.date_input(label="Date Range", key='RSmalb_Start')

        col_w4, col_w5 = st.columns(2, gap='medium')
        with col_w4:
            nSpan = st.slider(label='-ve Span', min_value=1, max_value=60, step=1, value=5, key='RSmalb4')
        with col_w5:
            pSpan = st.slider(label='+ve Span', min_value=1, max_value=60, step=1, value=5, key='RSmalb5')
        if st.button('Generate', use_container_width=True, key='RSmalb6'):
            RS_Extract.getlist_T3(index, [None, [pSpan, nSpan], time_frame, daterange])

#Check12
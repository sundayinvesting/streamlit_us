from github import Github
import requests
import pandas as pd
from pandas import DataFrame
import locale
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly

locale.setlocale(locale.LC_ALL, 'en_IN.utf8')


def graph_gen(chk):

    df = pd.DataFrame(data=chk,
                      columns=['Party Type', 'Party Name', 'Trans Type', 'Acquisition Date', 'Symbol', 'Company',
                               'No. of Share', 'Total Value (Rs)', 'Average Transaction Price (Rs)'])
    data = df.loc[:, ['Symbol', 'Trans Type', 'Total Value (Rs)']]
    dataS2 = data.groupby(['Symbol', 'Trans Type'])['Total Value (Rs)'].sum().reset_index(name='Net Value')
    dataS2['Net Value'] = round(dataS2['Net Value'] / 10000000, 2)
    pricedata = dataS2.values.tolist()
    stocklist = list(set(dataS2.iloc[:, 0].values.tolist()))
    buysell = []
    buylist = []
    selist = []
    for step in stocklist:  # _# List Separation
        buy, sell = 0.0, 0.0
        for part in pricedata:
            if step == part[0]:
                if part[1] == "Buy":
                    buy = part[2]
                if part[1] == "Sell":
                    sell = part[2]
        if buy > 0 and sell > 0:
            buysell.append([step, buy, sell])
        elif buy > 0 and sell == 0:
            buylist.append([step, buy])
        elif buy == 0 and sell > 0:
            selist.append([step, sell])
    BS_Gr100 = []
    BS_Ls100 = []
    for step in buysell:
        if step[1] > 100 or step[2] > 100:
            BS_Gr100.append(step)
        elif step[1] > 1 and step[2] > 1:  # _# Greater than 1 Cr for tickers less than 100 Cr
            BS_Ls100.append(step)

    BS_Gr100_df = pd.DataFrame(BS_Gr100, columns=['Stock', 'Buy', 'Sell']).sort_values('Stock', ascending=False)

    fig = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_xaxes=False,
                        shared_yaxes=True, horizontal_spacing=0)
    fig.append_trace(go.Bar(x=BS_Gr100_df['Buy'],
                            y=BS_Gr100_df['Stock'],
                            text=BS_Gr100_df['Buy'],
                            textposition='auto',
                            orientation='h',
                            width=0.7,
                            showlegend=False,
                            marker_color='#4472c4'), 1, 1)
    fig.append_trace(go.Bar(x=BS_Gr100_df['Sell'],
                            y=BS_Gr100_df['Stock'],
                            text=BS_Gr100_df['Sell'],
                            textposition='auto',
                            orientation='h',
                            width=0.7,
                            showlegend=False,
                            marker_color='#ed7d31'), 1, 2)
    fig.update_xaxes(showticklabels=False, title_text="Buy", row=1, col=1, autorange='reversed', title_standoff=60)
    fig.update_xaxes(showticklabels=False, title_text="Sell", row=1, col=2, title_standoff=60)
    fig.update_layout(title_text='Buy and Sell Position > 100 Cr. Rs')
    if len(BS_Gr100) > 10:
        fig.update_layout(height=len(BS_Gr100) * 40, autosize=True)
    if len(BS_Gr100) > 0:
        d1 = [fig.to_image(width=800), len(BS_Gr100)]
    else:
        d1 = None
    # ------------------------------------------------------------------------------------------------------------------

    BS_Ls100_df = pd.DataFrame(BS_Ls100, columns=['Stock', 'Buy', 'Sell']).sort_values('Stock', ascending=False)
    fig = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_xaxes=False, shared_yaxes=True, horizontal_spacing=0)
    fig.append_trace(go.Bar(x=BS_Ls100_df['Buy'],
                            y=BS_Ls100_df['Stock'],
                            text=BS_Ls100_df['Buy'],
                            textposition='auto',
                            orientation='h',
                            width=0.7,
                            showlegend=False,
                            marker_color='#4472c4'),1, 1)
    fig.append_trace(go.Bar(x=BS_Ls100_df['Sell'],
                            y=BS_Ls100_df['Stock'],
                            text=BS_Ls100_df['Sell'],
                            textposition='auto',
                            orientation='h',
                            width=0.7,
                            showlegend=False,
                            marker_color='#ed7d31'), 1, 2)
    fig.update_xaxes(showticklabels=False, title_text="Buy", row=1, col=1, autorange='reversed', title_standoff=60)
    fig.update_xaxes(showticklabels=False, title_text="Sell", row=1, col=2, title_standoff=60)
    fig.update_layout(title_text='Buy and Sell Position < 100 Cr. Rs')
    if len(BS_Ls100) > 10:
        fig.update_layout(height=len(BS_Ls100) * 40, autosize=True)
    if len(BS_Ls100) > 0:
        d2 = [fig.to_image(width=800), len(BS_Ls100)]
    else:
        d2 = None
    # ------------------------------------------------------------------------------------------------------------------
    buyfin = []
    for step in buylist:
        if step[1] > 0.5:
            buyfin.append(step)

    buyfin = sorted(buyfin, key=lambda x: x[1])
    df_buy = pd.DataFrame(buyfin, columns=['Stock', 'Buy'])
    # create subplots
    fig = make_subplots(rows=1, cols=1, specs=[[{}]], shared_xaxes=False,
                        shared_yaxes=False, horizontal_spacing=0)
    fig.append_trace(go.Bar(x=df_buy['Buy'],
                            y=df_buy['Stock'],
                            text=df_buy['Buy'],
                            textposition='auto',
                            orientation='h',
                            width=0.7,
                            showlegend=False,
                            marker_color='#4472c4'),1, 1)
    fig.update_layout(title_text='Buy Only Position > 0.5 Cr. Rs')
    if len(buyfin) > 10:
        fig.update_layout(height=len(buyfin) * 35)

    if len(buyfin) > 0:
        d3 = [fig.to_image(width=800),len(buyfin)]
    else:None

    selfin = []
    for step in selist:
        if step[1] > 0.5:
            selfin.append(step)
    # ------------------------------------------------------------------------------------------------------------------
    selfin = sorted(selfin, key=lambda x: x[1])
    df_sell = pd.DataFrame(selfin, columns=['Stock', 'Sell', ])
    fig = make_subplots(rows=1, cols=1, specs=[[{}]], shared_xaxes=False,
                        shared_yaxes=False, horizontal_spacing=0, )
    fig.append_trace(go.Bar(x=df_sell['Sell'],
                            y=df_sell['Stock'],
                            text=df_sell['Sell'],
                            textposition='auto',
                            orientation='h',
                            width=0.7,
                            showlegend=False,
                            marker_color='#4472c4'),1, 1)
    if len(selfin) > 10:
        fig.update_layout(height=len(selfin) * 35)

    fig.update_layout(title_text='Sell Only Position > 0.5 Cr. Rs')

    if len(selfin) > 0:
        d4 = [fig.to_image(width=800),len(selfin)]
    else:None

    return (d1, d2, d3, d4)


def data_push(start, end):
    # print(start,end)
    session = requests.Session()
    session.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0"

    session.get("https://www.nseindia.com/companies-listing/corporate-filings-insider-trading")

    result = session.get(
        "https://www.nseindia.com/api/corporates-pit?index=equities&from_date=%s&to_date=%s" % (start, end))

    src = result.json()

    Master = []
    for step in src['data']:
        temp = []
        # print(step)
        if step['secType'] == "Equity Shares":
            if step['personCategory'] == 'Promoters' or step['personCategory'] == 'Promoter Group':
                if step['tdpTransactionType'] == 'Buy' or step['tdpTransactionType'] == 'Sell':
                    if step['acqMode'] == 'Market Purchase' or step['acqMode'] == 'Market Sale':
                        temp.append(step['personCategory'])
                        temp.append((step['acqName']))
                        temp.append(step['tdpTransactionType'])
                        temp.append(step['acqfromDt'])
                        temp.append(step['symbol'])
                        temp.append(step['company'])
                        temp.append(float(step['secAcq']))
                        temp.append(float(step['secVal']))
                        try:
                            temp.append(round(float(step['secVal']) / float(step['secAcq']), 1))
                        except Exception as e:
                            print(e)
                            temp.append(0.00)

                        # temp.append(locale.currency(float(step['secAcq']), grouping=True, symbol=False))
                        # temp.append(locale.currency(float(step['secVal']), grouping=True)[:-3])
                        # try:
                        #     temp.append(
                        #         locale.currency(round(float(step['secVal']) / float(step['secAcq']), 0), grouping=True)[
                        #         :-3])
                        # except Exception as e:
                        #     print(e)
                        #     temp.append(0.00)
                        if float(step['secAcq']) > 0:
                            if round(float(step['secVal']) / float(step['secAcq']), 2) > 0:
                                Master.append(temp)
    # print(Master)
    graph = graph_gen(Master)
    for step in Master:
        # print(step)
        try:
            step[6] = locale.currency(float(step[6]), grouping=True,symbol=False)[:-3]
            step[7] = locale.currency(float(step[7]), grouping=True)[:-3]
            step[8] = locale.currency(float(step[8]), grouping=True)[:-1]
        except Exception as e:
            print(e)
            pass


    data = pd.DataFrame(data=Master,
                        columns=['Party Type', 'Party Name', 'Trans Type', 'Acquisition Date', 'Symbol', 'Company',
                                 'No. of Share', 'Total Value (Rs)', 'Average Transaction Price (Rs)'])
    # print(Master)

        # (step)


    # print(data)
    #csv_data=data.to_csv('G:\PyGit\Streamlit\Data.csv')
    # print(csv_data)

    # ----
    ACCESS_TOKEN = "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"
    GITHUB_REPO = "Streamlit"
    GIT_BRANCH = "main"
    FOLDER_EMPL_IN_GIT = "Directory/Promoter_Data.csv"

    # print(Master)

    def git_commit_push(access_tocken, github_repo, git_branch, content, folder_empl_in_git):
        g = Github(access_tocken)

        repo = g.get_user().get_repo(github_repo)

        all_files = []
        contents = repo.get_contents("")

        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            else:
                file = file_content
                all_files.append(str(file).replace('ContentFile(path="', '').replace('")', ''))

        # with open(initial_file, 'r') as file:
        # content = file.read()

        # Upload to github
        if folder_empl_in_git in all_files:
            contents = repo.get_contents(folder_empl_in_git)
            repo.update_file(contents.path, "Automate Test", content, contents.sha, branch=git_branch)
            return folder_empl_in_git + ' UPDATED'
        else:
            repo.create_file(folder_empl_in_git, "Automate Test", content, branch=git_branch)
            return folder_empl_in_git + ' CREATED'

    # git_commit_push(ACCESS_TOKEN, GITHUB_REPO, GIT_BRANCH, csv_data, FOLDER_EMPL_IN_GIT)
    return (data, graph)

#data_push("12-01-2023","12-04-2023")

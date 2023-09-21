import requests
from io import StringIO
import pandas as pd
def data_pull():
    token = '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'
    owner = 'sundayinvesting'
    repo = 'Streamlit'
    path = 'Directory/Promoter_Data.csv'

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
    df = pd.read_csv(string_io_obj,sep=",",index_col=0,)
    #df = script_list.reset_index()

    print(df)
    return df
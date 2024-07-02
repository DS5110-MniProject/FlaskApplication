from dash import Dash, html, dcc, dash_table, callback, Input, Output
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import sqlite3
import base64
from io import StringIO, BytesIO

# constants
features = [
    'Name',
    'Age',
    'City',
    'Salary',
    'JoinDate'
]
app = Dash()
app.title = 'DS 5110 Mini-Project'


def get_upload_component():
    return dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'solid',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=False
    )

@callback(
        Output('df', 'data'),
        Input('upload-data', 'contents'),
        Input('upload-data', 'filename'),
        Input('df', 'data')
)
def upload_callback(file, filename, df_json):
    if file is not None:
        ct, file_str = file.split(',')
        decoded = base64.b64decode(file_str)
        if decoded:
            bytes_obj = BytesIO(decoded)
            bytes_obj.seek(0)
            new_df = import_data(filename, bytes_obj)
            if df_json:
                df = pd.read_json(StringIO(df_json))
                df = pd.concat((df, new_df), ignore_index=True)
            else:
                df = new_df
            return df.to_json()
    
def import_data(filename, file_stream):## TODO REPLACE WITH GROUP 1,2, and 3 work
    if filename.endswith('.json'):
        return pd.read_json(file_stream)
    elif filename.endswith('.csv'):
        return pd.read_csv(file_stream)
    elif filename.endswith('.xlsx'):
        return pd.read_excel(file_stream)
    elif filename.endswith('.db'):
        with open("db_file.db", "wb") as f:
            f.write(file_stream.getbuffer())
        conn = sqlite3.connect("db_file.db")
        query = "SELECT name FROM sqlite_master WHERE type = 'table';"
        table_names = pd.read_sql_query(query, conn)['name'].tolist()
        if len(table_names) != 1:
            raise ValueError(f"Expected one table, found {len(table_names)}: {table_names}")
        else:
            query = f"SELECT * FROM {table_names[0]}"
            df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    else:
        raise NameError("Cannot read file.  Can only support .json, .csv, .xlsx, and .db extensions.")

def get_graph_options_component():
    return html.Div(
        id='graph-options',
        style={'width':'50%'},
        children = [
            html.Div(
                id="options-title",
                children="Choose the x and y axis"
            ),
            html.Div(id="menus",
                     style={
                         'width':'100%',
                         'display':'flex',
                         'flexDirection':'row',
                         'justifyContent':'space-around',
                     },
                     children=[
                         html.Div(id='menu-1',
                                  style={
                                      'width':'50%'
                                  },
                                  children=[
                                      dcc.Dropdown(
                                          placeholder='X Axis',
                                          id="x-select",
                                          options=features
                                      )
                                  ]),
                         html.Div(id='menu-2',
                                  style={
                                      'width':'50%'
                                  },
                                  children=[
                                      dcc.Dropdown(
                                          placeholder='Y Axis',
                                          id="y-select",
                                          options=features + ['count']
                                      )
                                  ]),
                        html.Button('Submit', id='graph-submit', style={'width':'50%'})
                     ]

            )
        ]
    )

def get_df_component():
    df = pd.DataFrame({
        'THIS':[x for x in range(10)],
        'IS':[x for x in range(10)],
        'THE':[x for x in range(10)],
        'DATAFRAME':[x for x in range(10)]
        })
    return html.Div(
        style={'width':'100%',
               'paddingTop':'50px'},
        children=[
        dash_table.DataTable(df.to_dict('records'), [{"name":i, "id":i} for i in df.columns], id="data-table")
        ]
        )
def get_graph_component():
    return html.Div(
        id='graph-wrapper',
        style={'height':'100%'},
        children=[
        dcc.Graph(figure=go.Figure(go.Line(x=np.arange(0, 100))))
        ]
    )
app.layout = html.Div(
    id='outer-box',
    style={
        'width':'100%',
        'height':'100%',
        'display':'flex',
        'flexDirection':'column'
    },
    children=[
        dcc.Store(id='df'),
        html.Div(id='options',
                 style={
                    'width':'100%',
                    'height':'30%',
                    'display':'flex',
                    'flexDirection':'row',
                    'justifyContent':'space-around'
                 },
                 children=[
                    get_upload_component(),
                    get_graph_options_component(),
                 ]
                 ),
        html.Div(id='main',
                 style={
                    'width':'100%',
                    'height':'70%',
                    'display':'flex',
                    'flexDirection':'row',
                    'justifyContent':'space-around'
                 },
                 children=[
                    get_df_component(),
                    get_graph_component()
                 ])
])

if __name__ == '__main__':
    app.run(debug=True)
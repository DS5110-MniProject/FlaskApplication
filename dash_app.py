from dash import Dash, html, dcc, dash_table, callback, Input, Output
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import sqlite3
import base64
from io import StringIO, BytesIO
from report import ReportGenerator
from data_prep.Data_Preprocessing import format_df, merge_files_and_format
from data_prep.File_imports import read_file
from data_prep.NaN import fix_NaN
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
        multiple=True
    )

@callback(
        Output('df', 'data'),
        Input('upload-data', 'contents'),
        Input('upload-data', 'filename'),
        Input('df', 'data')
)
def upload_callback(files, filenames, df_json):
    if files is not None:
        dfs = []
        if df_json:
            dfs.append(pd.read_json(StringIO(df_json)))
        for idx, file in enumerate(files):
            if file is not None:
                ct, file_str = file.split(',')
                decoded = base64.b64decode(file_str)
                if decoded:
                    bytes_obj = BytesIO(decoded)
                    bytes_obj.seek(0)
                    with open(filenames[idx], "wb") as f:
                        f.write(bytes_obj.getbuffer())
                    dfs.append(read_file(filenames[idx]))
        if len(dfs) != 0:
            merged = merge_files_and_format(dfs)
            merged_no_nans = fix_NaN(merged)
            return merged_no_nans.to_json()

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
                     ]

            )
        ]
    )

@callback(
    Output('y-axis', 'data'),
    Input('y-select', 'value')
)
def store_y(y_val):
    return y_val

@callback(
    Output('x-axis', 'data'),
    Input('x-select', 'value')
)
def store_x(x_val):
    return x_val

def get_df_component():
    return html.Div(
        id="data-table",
        style={'width':'100%',
               'paddingTop':'50px'},
        )

@callback(
        Output('data-table', 'children'),
        Input('df', 'data')
)
def df_callback(df_json):
    if df_json:
        df = pd.read_json(StringIO(df_json))
        return dash_table.DataTable(
            data=df.to_dict('records'), 
            columns=[{"name":i, "id":i} for i in df.columns], 
            editable=False,
            filter_action="native",
            sort_mode="multi",
            sort_action="native",
            row_deletable=False,
            page_action="native",
            page_current=0,
            page_size=10
        )

def get_graph_component():
    return dcc.Graph()

@callback(
    Output('graph-wrapper', 'children'),
    Input('df', 'data'),
    Input('x-axis', 'data'),
    Input('y-axis', 'data')
)
def graph_callback(df_json, x_axis, y_axis):
    if df_json and x_axis:
        if not y_axis:
            y_axis = None
        repo = ReportGenerator(pd.read_json(StringIO(df_json)))
        fig = repo.histogram(x_axis, y_axis)
        return fig
    else:
        return go.Figure()

# App Layout defines the element being show on screen. In this case, it is a single element page.
app.layout = html.Div(
    id='outer-box',
    style={
        'width':'100%',
        'height':'100%',
        'display':'flex',
        'flexDirection':'column'
    },
    children=[
        dcc.Store(id='df'), # Stores the current dataframe
        dcc.Store(id='x-axis'), # Stores the selection for plotted x axis
        dcc.Store(id='y-axis'), # Stores the selection for plotted y axis
        html.Div(id='options', # Div containing the first two elements: the uploading module, and the graph options
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
        
        get_df_component(), # returns the dataframe
        get_graph_component()
        ])

if __name__ == '__main__':
    app.run(debug=True)

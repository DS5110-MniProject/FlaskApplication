from dash import Dash, html, dcc, dash_table
import plotly.graph_objects as go
import numpy as np
import pandas as pd

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
        # Allow multiple files to be uploaded
        multiple=True
    )

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
        dash_table.DataTable(df.to_dict('records'), [{"name":i, "id":i} for i in df.columns])
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
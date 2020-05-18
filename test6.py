import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly_express as px
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import dash_daq as daq
import pandas as pd

app = dash.Dash(__name__)

df = pd.read_csv('C:/Users/user/Desktop/team4project/table_2.csv')
df2 = pd.read_csv('C:/Users/user/Desktop/team4project/dashPaperOdor_mean_Count_max.csv')


df['striped_date'] = df['Time_real'].str.rstrip('0123456789:')
df['time'] = df['Time_real'].str.lstrip('0123456789/')

app.layout = html.Div(
    children=[
        html.H1(children='中華電信智能廁所監控儀表板', style={
                'textAlign': 'center', 'fontSize': '300%', 'color': 'white'}),
        html.Div(
            children=[
                daq.LEDDisplay(
                    id='led1',
                    value=10,
                    color='white',
                    backgroundColor='black',
                    size=75,
                    label={
                        'label': '異味監測儀-1號機(單位：ppm)',
                        'style': {'color': 'yellow', 'fontSize': '30px'}
                    },
                    labelPosition='top'
                )

            ],
            style={'width': '33%', 'display': 'inline-block'}

        ),

        html.Div(
            children=[
                daq.LEDDisplay(
                    id='led2',
                    value=10,
                    color='white',
                    backgroundColor='black',
                    size=75,
                    label={
                        'label': '本日進出累積人次',
                        'style': {'color': 'yellow', 'fontSize': '30px'}
                    },
                    labelPosition='top'
                )
            ],
            style={'width': '33%', 'display': 'inline-block'}
        ),
        html.Div(
            children=[
                daq.LEDDisplay(
                    id='led3',
                    value=10,
                    color='white',
                    backgroundColor='black',
                    size=75,
                    label={
                        'label': '異味監測儀-2號機(單位：ppm)',
                        'style': {'color': 'yellow', 'fontSize': '30px'}
                    },
                    labelPosition='top'

                )

            ],
            style={'width': '33%', 'display': 'inline-block', 'float': 'right'}
        ),
        html.Div(
            children=[
                daq.LEDDisplay(
                    id='led4',
                    value=10,
                    color='white',
                    backgroundColor='black',
                    size=75,
                    label={
                        'label': '第一廁間：衛生紙(%)',
                        'style': {'color': 'yellow', 'fontSize': '30px'}
                    },
                    labelPosition='top'
                )

            ],
            style={'width': '33%', 'display': 'inline-block'}
        ),
        html.Div(
            children=[
                daq.LEDDisplay(
                    id='led5',
                    value=10,
                    color='white',
                    backgroundColor='black',
                    size=75,
                    label={
                        'label': '第二廁間：衛生紙(%)',
                        'style': {'color': 'yellow', 'fontSize': '30px'}
                    },
                    labelPosition='top'
                )

            ],
            style={'width': '33%', 'display': 'inline-block'}
        ),
        html.Div(
            children=[
                daq.LEDDisplay(
                    id='led6',
                    value=10,
                    color='white',
                    backgroundColor='black',
                    size=75,
                    label={
                        'label': '第三廁間：衛生紙(%)',
                        'style': {'color': 'yellow', 'fontSize': '30px'}
                    },
                    labelPosition='top'
                )

            ],
            style={'width': '33%', 'display': 'inline-block'}
        ),

        html.Div(
            children='', style={'height': '10px'}
        ),

        html.Div(
            children=[
                dcc.Dropdown(
                    id='dropdown',
                    options=[
                        {'label': i, 'value': i} for i in df['striped_date'].unique()
                    ],
                    placeholder='請選擇指定日期.'
                )
            ],
            style={'width': '50%', 'margin': 'auto'}

        ),

        html.Div(
            children=[
                html.H2('異味監測圖', style={
                        'textAlign': 'center', 'color': 'white'}),
                dcc.Graph(id='scatter_1')
            ],
            style={'width': '70%',
                   'margin': 'auto'
                   #    'display': 'inline-block'
                   },
        ),
        html.Div(
            children='', style={'height': '10px'}
        ),
        html.Div(
            children=[
                dcc.Dropdown(
                    id='dropdown2',
                    options=[
                        {'label': i, 'value': i} for i in df2['date'].unique()
                    ],
                    placeholder='請選擇指定日期.'
                )
            ],
            style={'width': '50%', 'margin': 'auto'}

        ),
        html.Div(
            children=[
                html.H2('異味與人流監測圖 (時間單位:半小時)', style={'textAlign': 'center','color':'white'}),
                dcc.Graph(id='scatter_2')
            ],
            style={'width': '70%',
                   'margin': 'auto'}
        ),
        dcc.Interval(
            id='interval-component',
            interval=2*1000,
            n_intervals=0
        )
    ],
    style={'backgroundColor': 'black'}

)


@app.callback(
    [Output('led1', 'value'),
     Output('led2', 'value'),
     Output('led3', 'value'),
     Output('led4', 'value'),
     Output('led5', 'value'),
     Output('led6', 'value')],
    [Input('interval-component', 'n_intervals')]
)
def update_meter(n):
    intime_df = pd.read_csv('C:/Users/user/Desktop/team4project/intime.csv')
    outOdr1 = intime_df[intime_df['id'] == 'G1F_W04_Odor']['value']
    outOdr2 = intime_df[intime_df['id'] == 'G1F_W05_Odor']['value']
    outCount = intime_df[intime_df['id'] == 'G1F_WomanCounting']['value']
    outPaper1 = intime_df[intime_df['id'] == 'G1F_W01_Paper']['value']
    outPaper2 = intime_df[intime_df['id'] == 'G1F_W02_Paper']['value']
    outPaper3 = intime_df[intime_df['id'] == 'G1F_W03_Paper']['value']
    
    return outOdr1,outCount,outOdr2,outPaper1, outPaper2, outPaper3


@ app.callback(
    Output('scatter_1', 'figure'),
    [Input('dropdown', 'value')]
)
def update_figure_1(dropdown_value):
    filtered_df = df[df['striped_date'] == dropdown_value]

    traces_1 = go.Scatter(
        x=filtered_df['time'].values,
        y=filtered_df['Odr_1'].values,
        text=filtered_df['time'],
        mode='lines',
        line={'color': 'red'},
        opacity=0.7,
        name='異味監測儀-1號機')

    traces_2 = go.Scatter(
        x=filtered_df['time'].values,
        y=filtered_df['Odr_2'].values,
        text=filtered_df['time'],
        mode='lines',
        line={'color': 'blue'},
        opacity=0.7,
        name='異味監測儀-2號機'
    )
    layout = go.Layout(
        xaxis={'title': {'text': '時間', 'font': {
            'size': 20}}, 'automargin': True, 'rangemode': 'tozero', 'ticks': 'inside', 'tickangle': 60},
        yaxis={'title': {'text': '異味值(ppm)',
                         'font': {'size': 20}}, 'automargin': True, 'rangemode': 'tozero', 'ticks': 'inside'},
        legend={'x': 0, 'y': 1},

        # hovermode='closest'
    )
    return go.Figure(
        data=[traces_1, traces_2],
        layout=layout
    )
@ app.callback(
    Output('scatter_2', 'figure'),
    [Input('dropdown2', 'value')]
)
def update_figure_2(dropdown_value):
    filtered_df_2 = df2[df2['date'] == dropdown_value]

    traces_3 = go.Scatter(
        x=filtered_df_2['time'].values,
        y=filtered_df_2['Odr_1'].values,
        text=filtered_df_2['time'],
        mode='lines',
        line={'color': 'red'},
        opacity=0.7,
        name='異味監測儀-1號機')

    traces_4 = go.Scatter(
        x=filtered_df_2['time'].values,
        y=filtered_df_2['Odr_2'].values,
        text=filtered_df_2['time'],
        mode='lines',
        line={'color': 'blue'},
        opacity=0.7,
        name='異味監測儀-2號機'
    )
    traces_5 = go.Bar(
        x=filtered_df_2['time'].values,
        y=filtered_df_2['Count'].values,
        text=filtered_df_2['time'],
        name='人流累計'
    )
    layout = go.Layout(
        xaxis={'title': {'text': '時間', 'font': {
            'size': 20}}, 'automargin': True, 'rangemode': 'tozero', 'ticks': 'inside', 'tickangle': 60},
        yaxis={'title': {'text': '異味值(ppm)',
                         'font': {'size': 20}}, 'automargin': True, 'rangemode': 'tozero', 'ticks': 'inside'},
        
        legend={'x': 0, 'y': 1},

        # hovermode='closest'
    )
    return go.Figure(
        data=[traces_3, traces_4,traces_5],
        layout=layout
    )
if __name__ == '__main__':
    app.run_server(debug=True)

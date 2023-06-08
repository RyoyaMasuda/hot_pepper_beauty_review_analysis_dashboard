from dash import Dash, dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly
import plotly.express as px
import plotly.figure_factory as ff
import scipy

from navber import navber

default_font='Comic Sans Ms'

df = pd.read_csv('./data/merge_df.csv', low_memory=False)


app = Dash(__name__,
           suppress_callback_exceptions=True,
           prevent_initial_callbacks=False,
           external_stylesheets=[dbc.themes.DARKLY])

sidebar = html.Div(
    [
        dbc.Row(
            html.P(
                children='Select the parameters.',
                style={'margin':'10px', 'fontSize':20},
            ),
            className='bg-secondary'
        ),
        dbc.Row(
            [
                html.P(
                    children='Select a prefecture',
                    style={'margin': '10px', 'width':'175px'},
                    className='border-bottom font-weight-bold'
                ),
                dcc.Dropdown(
                    id='dropdown1',
                    options=[
                        {'label':x, 'value':x} for x in df['県'].unique()
                    ],
                    value='広島',
                    style={'width':'250px', 'margin-bottom':'1px', 'fontSize':15},
                    clearable=True,
                    className='text-dark'
                ),
                html.P(
                    children='Select a region',
                    style={'margin': '10px', 'width':'140px'},
                    className='border-bottom font-weight-bold'
                ),
                dcc.Dropdown(
                    id='dropdown2',
                    # options = callbackで返ってくる。
                    style={'width':'250px', 'margin-bottom':'1px', 'fontSize':15},
                    clearable=True,
                    value='八丁堀・幟町・胡町',
                    className='text-dark',
                ),
                html.P(
                    children='Select a salon',
                    style={'margin': '10px', 'width':'130px'},
                    className='border-bottom font-weight-bold'
                ),
                dcc.Dropdown(
                    id='dropdown3',
                    # options = callbackで返ってくる。
                    value='ATENA　AVEDA　広島三越店 【アテナアヴェダ】',
                    style={'width':'250px', 'margin-bottom':'1px', 'fontSize':12},
                    clearable=True,
                    # 各オプションの高さ。ラベルの長さが回り込むような場合は、大きくすることができます。
                    optionHeight=45,
                    className='text-dark'
                ),
                html.P(
                    children='Select gender',
                    style={'margin': '10px', 'width':'130px'},
                    className='border-bottom font-weight-bold'
                ),
                dcc.Checklist(
                    id='checklist1',
                    # options = callbackで返ってくる。
                    value=['女性', '未設定', '男性'],
                    inline=True,
                    inputStyle={'margin':'8px'}
                ),
                dbc.Button(
                    id='button',
                    children='Apply',
                    color='info',
                    n_clicks=0,
                    style={'margin':'20px'},
                    className='d-grid gap-2 col-6 mx-auto',
                ),
                html.Hr()
            ]
        )
    ],
    style={'font-family': 'Comic Sans Ms'}
)

content = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(
                            id='gender-rate',
                            # figureの大きさは最初から指定しておく。
                            figure={'layout':{'height':260, 'width':375}},
                            # style={'margin-top':'10px',
                            #        'margin-bottom':'10px',
                            #        'margin-right':'2px',
                            #        'margin-left':'2px'}
                        )                     
                ],
                className='bg-info col-3',
                style={'padding':'10px'
                    }
                ),
                dbc.Col(
                    [
                        dcc.Graph(
                            id='age-rate',
                            # figureの大きさは最初から指定しておく。
                            figure={'layout':{'height':260, 'width':375}},
                            # margin-*の順番によって反映されないことがある。原因不明。leftよりもrightが先に来ると反応しなかった。上のdbc.Colは何故か大丈夫
                            # style={'margin-top':'10px',
                            #        'margin-bottom':'10px',
                            #        'margin-left':'1px',
                            #        'margin-right':'px'
                            #     }
                        )
                ],
                    # 画面のワイドの設定はcol-**で設定した方がいい。横が12だからcol−６で半分
                className='bg-light col-3',
                style={'padding':'0.7%'}
                ),
                dbc.Col(
                    [
                        ],
                    className='bg-info col-6',
                    style={'padding':'0.7%'}
                ),
            ],
            className='bg-primary',
            style={'height':'30vh'}
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(
                            id='total_bill_distplot',
                            figure={'layout':{'height':360, 'width':775}},
                        )
                ],
                    className='bg-warning',
                    style={'padding':'0.6%'}
                ),
                dbc.Col(
                    [
                        ],
                    className='bg-light'
                    ),
            ],
            # className='bg-secondary',
            style={'height':'40vh'}
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
      
                ],
                    className='bg-info'
                    ),
                dbc.Col(
                    [
                        ],
                    className='bg-light'
                    ),
            ],
            className='bg-light',
            style={'height':'30vh'}
        )   
    ]
)

home_layout = [
    dbc.Row(
        [
            dbc.Col(
                children=sidebar,
                width=2,
                className='bg-primary'
            ),
            dbc.Col(
                children=content,
                width=10,
                className='bg-light'
            )
        ],
        style={'height':'95vh'}
    )
]

app.layout = dbc.Container(
    [
        dbc.Row(
            children=navber
        ),
        html.Div(
            id='layout',
            children=home_layout
        )
    ],
    fluid=True
)

@app.callback(
    Output('dropdown2', 'options'),
    Input('dropdown1', 'value')
)
def update_area(value):
    return [{'label': x2,'value': x2} for x2 in df[df['県'] == value]['エリア'].unique()]

@app.callback(
    Output('dropdown3', 'options'),
    Input('dropdown2', 'value')
)
def update_salon(value):
    return [{'label': x3,'value': x3} for x3 in df[df['エリア'] == value]['サロン名'].unique()]

@app.callback(
    Output('checklist1', 'options'),
    Input('dropdown3', 'value'),
    State('dropdown2', 'value')
)
def update_gender(dropdown3_value, dropdown2_value):
    _df = df[df['エリア'] == dropdown2_value]
    _df = _df[_df['サロン名'] == dropdown3_value]
    return [{'label': x3,'value': x3} for x3 in _df['性別'].unique()]

@app.callback(
    Output('gender-rate', 'figure'),
    Input('button', 'n_clicks'),
    [State('dropdown1', 'value'),
     State('dropdown2', 'value'),
     State('dropdown3', 'value'),
     State('checklist1', 'value')])
def gender_rate_figure(n_clicks, dropdown1_value, dropdown2_value, dropdown3_value, checklist1_value):
    
    _df = df.copy()
    _df = _df[_df['県']==dropdown1_value]
    _df = _df[_df['エリア'] == dropdown2_value]
    _df = _df[_df['サロン名'] == dropdown3_value]
    
    _df = _df[_df['性別'].isin(checklist1_value)]
    
    _df =_df.groupby('性別').count().iloc[:,0:1].reset_index()
    _df.rename(columns={'県':'客数(口コミ数)'}, inplace=True)
    figure = px.pie(
        data_frame=_df,
        names='性別',
        values='客数(口コミ数)',
        color='性別',
        title=f'Gender Rate',
        height=260,
        width=375,
        color_discrete_map={'女性':'skyblue','男性':'peachpuff','未設定':'palegreen'},
    )
    
    figure.update_traces(
        textinfo='percent+label',
        textposition='inside',
        marker=dict(
            line=dict(
                color='slategrey',
                width=2.0
            ),
        )
    )
    
    figure.update_layout(
        uniformtext_mode='hide',
        uniformtext_minsize=10,
        margin={'l':30, 'r':30, 't':50, 'b':10},
        title={'font':{'size':20,
                       'color':'grey'},
               'x':0.5,
               'y':0.95,
               'xanchor':'center'},
        font=dict(
            family='Comic Sans Ms',
            size=10,
        ),
        # hoverlabel: hoverdataの中の指定
        hoverlabel=dict(font=dict(family="Comic Sans Ms",
                                  size=12,
                                #   color="white"
                                  )
                        ),
        paper_bgcolor='lightcyan',
        # autosize=True,
        legend=dict(
            title=dict(text='性別',
                       font=dict(family=default_font,
                                 size=12),
            ),
            bgcolor='aliceblue',
            bordercolor='grey',
            #bordercolorを指定したらborderwidthも指定しないといけない。
            borderwidth=2,
            font=dict(size=12,
                      family=default_font,
                      color='slategrey'),
        ),
        
    )
    
    return figure
    
@app.callback(
    Output('age-rate', 'figure'),
    Input('button', 'n_clicks'),
    [State('dropdown1', 'value'),
     State('dropdown2', 'value'),
     State('dropdown3', 'value'),
     State('checklist1', 'value')])
def age_rate_figure(n_clicks, dropdown1_value, dropdown2_value, dropdown3_value, checklist1_value):
        
    _df = df.copy()
    _df = _df[_df['県']==dropdown1_value]
    _df = _df[_df['エリア'] == dropdown2_value]
    _df = _df[_df['サロン名'] == dropdown3_value]
    
    _df = _df[_df['性別'].isin(checklist1_value)]
    
    _df = _df.groupby('年齢').count().iloc[:,0:1].reset_index()
    _df.rename(columns={'県':'客数(口コミ数)'}, inplace=True)
    figure = px.pie(
        data_frame=_df,
        names='年齢',
        values='客数(口コミ数)',
        color='年齢',
        title='Age Rate',
        height=260,
        width=375,
        # color_discrete_map={'女性':'cornflowerblue','男性':'hotpink','未設定':'darkorange'},
        color_discrete_sequence=plotly.colors.qualitative.Set3,
        category_orders={'年齢':['～10代前半', '10代後半', '20代前半', '20代後半', '30代前半', '30代後半', '40代', '50代', '60代', '70代～', '未設定']}
    )
    
    figure.update_traces(
        textinfo='percent+label',
        textposition='inside',
        marker=dict(
            line=dict(
                color='slategrey',
                width=2.0
            ),
        ),
        # legendgrouptitle=dict(
        #     font=dict(
        #         size=30
        #     )
        # )
    )
    
    figure.update_layout(
        uniformtext_mode='hide',
        uniformtext_minsize=10,
        margin={'l':30, 'r':30, 't':50, 'b':10},
        title={'font':{'size':20,
                       'color':'grey'},
               'x':0.5,
               'y':0.95,
               'xanchor':'center'},
        font=dict(
            family='Comic Sans Ms',
            size=10,
        ),
        # hoverlabel: hoverdataの中の指定
        hoverlabel=dict(font=dict(family="Comic Sans Ms",
                                  size=12,
                                #   color="white"
                                  )
                        ),
        paper_bgcolor='lightcyan',
        # ユーザーによって未定義にされたレイアウトの幅や高さを、各リレーアウトで初期化するかどうかを決定します。この属性に関係なく、未定義のレイアウトの幅や高さは、plotの最初の呼び出しで常に初期化されることに注意してください。
        # autosize=True,
        legend=dict(
            title=dict(text='年齢',
                       font=dict(family=default_font,
                                 size=12),
            ),
            bgcolor='aliceblue',
            bordercolor='grey',
            #bordercolorを指定したらborderwidthも指定しないといけない。
            borderwidth=2,
            font=dict(size=12,
                      family=default_font,
                      color='slategrey'),
            # valign='top',
            itemsizing='constant'
        ),
        
    )
    
    return figure

@app.callback(
    Output('total_bill_distplot', 'figure'),
    Input('button', 'n_clicks'),
    [State('dropdown1', 'value'),
     State('dropdown2', 'value'),
     State('dropdown3', 'value'),
     State('checklist1', 'value')])
def total_bill_distplot_figure(n_clicks, dropdown1_value, dropdown2_value, dropdown3_value, checklist1_value):
            
    _df = df.copy()
    _df = _df[_df['県']==dropdown1_value]
    _df = _df[_df['エリア'] == dropdown2_value]
    _df = _df[_df['サロン名'] == dropdown3_value]
    
    _df = _df[_df['性別'].isin(checklist1_value)]
    
    _df = _df[['年齢', '支出金額', '名前', 'メニューの種類', '性別', '職業', '投稿日時','総合','雰囲気','接客サービス',	'技術・仕上がり', 'メニュー・料金']][_df['支出金額']!=0]
    
    figure = px.box(_df, y="支出金額", x="年齢", color="年齢", points="all",
          hover_data=_df.columns, title='Distribution of Payments by Age',
          color_discrete_sequence=plotly.colors.qualitative.Set3,
          category_orders={'年齢':['～10代前半', '10代後半', '20代前半', '20代後半', '30代前半', '30代後半', '40代', '50代', '60代', '70代～', '未設定']}
          )

    figure.update_traces(
        marker=dict(
            line=dict(
                color='grey',
                width=1.0
            ),
            size=5,
            opacity=0.9
        ),
    )

    figure.update_yaxes(
        rangemode='tozero',
        tickformat=',',
        tickprefix='¥',
        tickvals=[0,2500,5000,7500,10000,12500,15000,17500,20000,25000,30000,40000]
    )

    figure.update_layout(
        uniformtext_mode='hide',
        uniformtext_minsize=10,
        margin={'l':30, 'r':30, 't':50, 'b':10},
        title={'font':{'size':20,
                       'color':'grey'},
               'x':0.5,
               'y':0.95,
               'xanchor':'center'},
        font=dict(
            family='Comic Sans Ms',
            size=10,
        ),
        # hoverlabel: hoverdataの中の指定
        hoverlabel=dict(font=dict(family="Comic Sans Ms",
                                  size=12,
                                #   color="white"
                                  )
                        ),
        paper_bgcolor='lightcyan',
        # ユーザーによって未定義にされたレイアウトの幅や高さを、各リレーアウトで初期化するかどうかを決定します。この属性に関係なく、未定義のレイアウトの幅や高さは、plotの最初の呼び出しで常に初期化されることに注意してください。
        # autosize=True,
        legend=dict(
            title=dict(text='年齢',
                       font=dict(family=default_font,
                                 size=12),
            ),
            bgcolor='aliceblue',
            bordercolor='grey',
            #bordercolorを指定したらborderwidthも指定しないといけない。
            borderwidth=2,
            font=dict(size=12,
                      family=default_font,
                      color='slategrey'),
            # valign='top'
            itemsizing='constant'
        ),
        
    )
    
    return figure

@app.callback(
    [Output('layout', 'children')],
    [Input('url', 'pathname')]
)
def update_page(href):
    if href == '/':
        return home_layout
    
if __name__ == '__main__':
    app.run_server(debug=True, port=8049)
# imports

import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output



# initialize dataframes
root = '../covid_meta/'
df_meta = pd.read_csv(root+'covid_19_data.csv')
df_US = pd.read_csv(root+'time_series_covid_19_confirmed_US.csv')

# get total cases
last_update = '2020-11-16 05:25:57'
sub = df_meta[df_meta['Last Update'] == last_update]
tot_cases = sum(sub['Confirmed'])

# heatmap plot (no interactions)
dfheat = df_meta.copy()
dfheat['monthday'] = pd.DatetimeIndex(dfheat['ObservationDate']).is_month_end
dfheat.loc[dfheat['ObservationDate'] == '11/15/2020', 'monthday'] = True
dfheat = dfheat[dfheat['monthday'] == True]
dfheat = dfheat.groupby(['Country/Region','ObservationDate'])[['Confirmed']].sum().reset_index()
tops = dfheat[dfheat['ObservationDate'] == '11/15/2020'].sort_values(by='Confirmed', ascending=False).head(10)
tops = tops['Country/Region'].tolist()
dfheat = dfheat[dfheat['Country/Region'].isin(tops)]
counts = []
for i in tops:
    counts.append(dfheat[dfheat['Country/Region'] == i]['Confirmed'].tolist())
nc = []
for i in counts:
    tmp = []
    if len(i) != 11:
        for c in range(11-len(i)):
            tmp.append(0)
    for j in range(1,len(i)):
        tmp.append(i[j] - i[j-1])
    nc.append(tmp)
heatmap = px.imshow(nc[:5], labels=dict(x='Month', y='Country', color='Number of Cases'),
        x=['January', 'March', 'April', 'May', 'June','July','August','September','October','November'],
        y=tops[:5]
)
heatmap.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                    title={'text':'Monthly Case Count of Top 5 COVID-Affected Countries in 2020',
                            'y':0.9, 'x':0.5, 'xanchor':'center', 'yanchor':'top'})

# initialize app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# layout
app.layout = html.Div([

    dbc.Row([
        dbc.Col([
            html.H1('COVID-19 Dashboard', style={'text-align': 'center', 'color':'#ffffff', 'margin':'0', 'font-size':'300%'}),
            html.H2('Last Updated: 11/16/20', style={'text-align':'center', 'color':'#008080', 'font-size':'100%'})
        ], lg=6, md=6),
        dbc.Col([
            html.Div([
                html.H3('Total Cases', style={'font-size':'120%', 'color':'#ffffff'}),
                html.P('{:,.0f}'.format(tot_cases), style={'font-size':'200%', 'color':'#00ffff'})
            ], style={'text-align':'center', 'border':'2px solid #00ffff', 'border-radius':'10px', 'padding':'20px 20px 0px 20px'})
        ], sm=12, lg=3, md=6)
    ], justify='end'),
    
    
    
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id='bubbledrop', 
                         options=[{'label': 'Confirmed', 'value': 'Confirmed'}, {'label': 'Deaths', 'value': 'Deaths'}], 
                         value='Confirmed'),
            html.P(id='bubbletext', children=[], style={'color':'white', 'text-align':'center'}),
            dcc.Graph(id='graph', figure={}, style={'margin-top':'-65px', 'text-align':'center'})
        ], lg=2, sm={'size':7, 'order':'first'}, style={'margin-top':'10px'}),

        dbc.Col([  
            dcc.Graph(id='timegraph', figure={})
        ], lg={'size':8, 'order':1}, sm={'size':12, 'order':'last'}, xs={'size':12, 'order':'last'}),

        dbc.Col([
            dcc.RadioItems(
                id='whichtime',
                options=[
                    {'label': 'New Cases', 'value': 'New Cases'},
                    {'label': 'Cumulative Cases', 'value': 'Cumulative Cases'}
                ],
                value='Cumulative Cases',
                labelStyle={'display':'block', 'color':'white'},
                inputStyle={'margin-right':'5px'}
            ),
            dcc.Dropdown(
                id='states',
                options=[
                    {'label': 'Alabama', 'value': 'Alabama'},
                    {'label': 'Alaska', 'value': 'Alaska'},
                    {'label': 'Arizona', 'value': 'Arizona'},
                    {'label': 'Arkansas', 'value': 'Arkansas'},
                    {'label': 'California', 'value': 'California'},
                    {'label': 'Colorado', 'value': 'Colorado'},
                    {'label': 'Connecticut', 'value': 'Connecticut'},
                    {'label': 'Delaware', 'value': 'Delaware'},
                    {'label': 'Florida', 'value': 'Florida'},
                    {'label': 'Georgia', 'value': 'Georgia'},
                    {'label': 'Hawaii', 'value': 'Hawaii'},
                    {'label': 'Idaho', 'value': 'Idaho'},
                    {'label': 'Illinois', 'value': 'Illinois'},
                    {'label': 'Indiana', 'value': 'Indiana'},
                    {'label': 'Iowa', 'value': 'Iowa'},
                    {'label': 'Kansas', 'value': 'Kansas'},
                    {'label': 'Kentucky', 'value': 'Kentucky'},
                    {'label': 'Louisiana', 'value': 'Louisiana'},
                    {'label': 'Maine', 'value': 'Maine'},
                    {'label': 'Maryland', 'value': 'Maryland'},
                    {'label': 'Massachusetts', 'value': 'Massachusetts'},
                    {'label': 'Michigan', 'value': 'Michigan'},
                    {'label': 'Minnesota', 'value': 'Minnesota'},
                    {'label': 'Mississippi', 'value': 'Mississippi'},
                    {'label': 'Missouri', 'value': 'Missouri'},
                    {'label': 'Montana', 'value': 'Montana'},
                    {'label': 'Nebraska', 'value': 'Nebraska'},
                    {'label': 'Nevada', 'value': 'Nevada'},
                    {'label': 'New Hampshire', 'value': 'New Hampshire'},
                    {'label': 'New Jersey', 'value': 'New Jersey'},
                    {'label': 'New Mexico', 'value': 'New Mexico'},
                    {'label': 'New York', 'value': 'New York'},
                    {'label': 'North Carolina', 'value': 'North Carolina'},
                    {'label': 'North Dakota', 'value': 'North Dakota'},
                    {'label': 'Ohio', 'value': 'Ohio'},
                    {'label': 'Oklahoma', 'value': 'Oklahoma'},
                    {'label': 'Oregon', 'value': 'Oregon'},
                    {'label': 'Pennsylvania', 'value': 'Pennsylvania'},
                    {'label': 'Rhode Island', 'value': 'Rhode Island'},
                    {'label': 'South Carolina', 'value': 'South Carolina'},
                    {'label': 'South Dakota', 'value': 'South Dakota'},
                    {'label': 'Tennessee', 'value': 'Tennessee'},
                    {'label': 'Texas', 'value': 'Texas'},
                    {'label': 'Utah', 'value': 'Utah'},
                    {'label': 'Vermont', 'value': 'Vermont'},
                    {'label': 'Virginia', 'value': 'Virginia'},
                    {'label': 'Washington', 'value': 'Washington'},
                    {'label': 'West Virginia', 'value': 'West Virginia'},
                    {'label': 'Wisconsin', 'value': 'Wisconsin'},
                    {'label': 'Wyoming', 'value': 'Wyoming'}
                ],
                value=['California', 'New Jersey'],
                placeholder='Select States',
                multi=True,
                clearable=False
            )  
        ], md={'size':9, 'order':1}, lg={'size':2, 'order':'last'})
    ], justify='center'),

    dbc.Row([
        dbc.Col([
            html.A('View Data Source', href='https://www.kaggle.com/sudalairajkumar/novel-corona-virus-2019-dataset', target='_blank'),
            html.Br(),
            html.A('View Source Code', href='https://github.com/luluricketts/COVID19', target='_blank')
        ], lg={'size':2, 'order':'first'}, sm={'size':12, 'order':'last'}, style={'text-align':'center'}, xs={'size':12,'order':'last'}),
        dbc.Col([
            dcc.Graph(id='heat', figure=heatmap)
        ], lg={'size':8, 'offset':2, 'order':'last'}, sm={'size':12, 'order':'first'})
    ])

], style={'background-color':'black', 'padding':'1rem', 'font-family':'Gayathri'})


# callback functions
@app.callback(
    [Output(component_id='graph', component_property='figure'),
     Output(component_id='bubbletext', component_property='children')],
    [Input(component_id='bubbledrop', component_property='value')]
)
def update_bubbles(option):

    text = 'Top 20 Countries With Highest {} Cases'.format(option)

    last_update = '2020-11-16 05:25:57'
    dff = df_meta.copy()
    dff = dff[dff['Last Update'] == last_update]
    drop_cols = ['SNo', 'ObservationDate', 'Last Update']
    dff.drop(columns=drop_cols, inplace=True, axis=1)
    dff = dff.groupby('Country/Region')[['Confirmed','Deaths']].sum().sort_values(by=option,ascending=False).reset_index().head(20)

    dff['x'] = 0.5**dff.index
    dff['y'] = dff.index

    options = {'Confirmed':0, 'Deaths':1}
    colors = [px.colors.sequential.Emrld, px.colors.sequential.Burg]

    fig = px.scatter(dff, x='x', y='y', size=option, color=option, hover_name='Country/Region',
                 color_continuous_scale=colors[options[option]], 
                 text='Country/Region', size_max=60, width=400, height=800,
                 hover_data={
                     'x':False, 'y':False, 'Country/Region':False
                 })

    fig.update_traces(textfont=dict(family='Gayathri', color='white'))
    fig.update_layout(xaxis={'showgrid':False, 'zeroline':False, 'visible':False, 'range':[-.5, 2]}, 
                     yaxis={'showgrid':False, 'zeroline':False, 'visible':False},
                     paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    fig.update_coloraxes(colorbar=dict(yanchor="top", y=0.99, xanchor="left", x=-.35))
    
    return fig, text

@app.callback(
    Output(component_id='timegraph', component_property='figure'),
    [Input(component_id='whichtime', component_property='value'),
    Input(component_id='states', component_property='value')]
)
def update_timegraph(which, states):

    if len(states) == 0:
        return {
            "layout": {
                "xaxis": {"visible": False},
                "yaxis": {"visible": False},
                "annotations": [{
                        "text": "Please select at least 1 state",
                        "showarrow": False,
                        "font": {"size": 28}}]
        }}

    df = df_US.copy()
    time_cols = df_US.columns[11:]
    df = df[df['Province_State'].isin(states)]
    df = df.groupby('Province_State')[time_cols].sum().T
    df.columns.name = 'State'
    print(df.info())

    if which == 'Cumulative Cases':
        fig = px.line(df, x=df.index, y=df.columns)
        fig.update_layout(xaxis={'showgrid':False}, 
                        yaxis={'showgrid':False},
                        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                        title={
                            'text':'United States Cumulative Cases by State',
                            'y':0.9,
                            'x':0.5,
                            'xanchor':'center',
                            'yanchor':'top'
                        },
                        font_color='#008080',
                        xaxis_title='Date',
                        yaxis_title='Count')
    else:
        new = dict()
        for col in df.columns:
            new[col] = [df[col][i]-df[col][i-1] if df[col][i]-df[col][i-1] >= 0 else 0 for i in range(1, len(df))]
        dfn = pd.DataFrame(new)
        dfn.index = df.index[1:]
        dfn.columns.name = 'State'
        print(len(dfn), dfn.index, dfn.columns)
        fig = px.line(dfn, x=dfn.index, y=dfn.columns, labels={
            'index': 'Date', 'value':'Count'
        })
        fig.update_layout(xaxis={'showgrid':False}, 
                        yaxis={'showgrid':False},
                        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                        title={
                            'text':'United States Cumulative Cases by State',
                            'y':0.9,
                            'x':0.5,
                            'xanchor':'center',
                            'yanchor':'top'
                        },
                        font_color='#008080')
    return fig





# run server
if __name__ == '__main__':
    app.run_server(debug=True)
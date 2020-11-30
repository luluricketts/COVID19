# imports

import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output



# initialize dataframes
root = 'covid_meta/'

# complete data
df_meta = pd.read_csv(root+'covid_19_data.csv')
drop_cols = ['SNo', 'ObservationDate', 'Last Update']
df_meta.drop(columns=drop_cols, inplace=True, axis=1)

# dataframe for bubble scatter plot
country = pd.DataFrame(df_meta.groupby('Country/Region')[['Confirmed','Deaths']].sum().sort_values(by='Confirmed',ascending=False))
country = country.reset_index()

# initialize app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# layout
app.layout = html.Div([
    
    html.H1('COVID-19 Dashboard', style={'text-align': 'right', 'color':'#72C0F3'}),
    html.H2('Last Updated: 11/15/20', style={'text-align':'right', 'color':'#5B9BC4'}),
    
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id='bubbledrop', 
                         options=[{'label': 'Confirmed', 'value': 'Confirmed'}, {'label': 'Deaths', 'value': 'Deaths'}], 
                         value='Confirmed'),
            html.P(id='bubbletext', children=[], style={'color':'white'}),
            dcc.Graph(id='graph', figure={}, style={'margin-top':'-70px'})
        ], width=2, style={'margin-top':'-100px'}),
        dbc.Col(html.H3('column 2'), width=4),
        dbc.Col(html.H3('column 3'), width=4)
    ], style={'text-align':'center'})
], style={'background-color':'black', 'padding':'1rem', 'font-family':'Gayathri'})


# callback functions
@app.callback(
    [Output(component_id='graph', component_property='figure'),
     Output(component_id='bubbletext', component_property='children')],
    [Input(component_id='bubbledrop', component_property='value')]
)
def update_bubbles(option):

    text = 'Top 20 Countries With Highest {} Cases'.format(option)

    dff = country.copy()
    dff = dff.sort_values(by=option, ascending=False).reset_index(drop=True).head(20)
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
    fig.update_coloraxes(colorbar=dict(yanchor="top", y=0.99, xanchor="left", x=-.25))
    
    return fig, text


# run server
if __name__ == '__main__':
    app.run_server(debug=True)
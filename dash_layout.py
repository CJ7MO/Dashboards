import pandas as pd
import dash
import plotly_express as px
from dash import html, dcc, Output, Input, State

#agregando el dataframe
df = pd.DataFrame({
    'fruit':['apples', 'oranges', 'bananas', 'apples', 'oranges', 'bananas'],
    'amount':[4, 1, 2, 2, 4, 5],
    'city': ['SF', 'SF', 'SF', 'NYC', 'MTL', 'NYC']
})

#creando la aplicacion
app = dash.Dash('__name__')

app.config.suppress_callback_exceptions = True


#diseñando la aplicacion
app.layout = html.Div(children=[
    html.H1(
        children='Dashboard',
        style={'textAlign':'center'}
    ),
    #creando lista desplegable
    dcc.Dropdown(id='input-city',
                 options=[
        {'label': 'New York City', 'value': 'NYC'},
        {'label': 'Montréal', 'value': 'MTL'},
        {'label': 'San Francisco', 'value':'SF'}
    ],
    placeholder='select city',
    style={'width':'100%', 'padding':'3px', 'font-size': '20px', 'text-align-last' : 'center'}
    ),
    #grafico de barras
    html.Div([ ], id='bar-plot')
])

@app.callback(Output(component_id='bar-plot', component_property='children'),
             Input(component_id='input-city', component_property='value'),
             State('bar-plot', 'children'))


def graph_function(value, plot):
    if value == 'NYC':
        df_nyc = df[df['city'] == 'NYC'].reset_index()
        df_nyc = df_nyc
        fig1 = px.bar(df_nyc, x='fruit', y='amount', color='fruit')
        return [dcc.Graph(figure=fig1)]
    if value == 'MTL':
        df_mtl = df[df['city'] == 'MTL'].reset_index()
        df_mtl = df_mtl
        fig2 = px.bar(df_mtl, x='fruit', y='amount', color='fruit')
        return [dcc.Graph(figure=fig2)]
    if value == 'SF':
        df_sf = df[df['city'] == 'SF'].reset_index()
        df_sf = df_sf
        fig3 = px.bar(df_sf, x='fruit', y='amount', color='fruit')
        return [dcc.Graph(figure=fig3)]
    else:
        fig = px.bar(df, x='fruit', y='amount', color='city', barmode='group')
        return [dcc.Graph(figure=fig)]


#ejecutar la aplicacion
if __name__ == '__main__':
    app.run_server(port='8080')
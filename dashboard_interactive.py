import pandas as pd
import plotly.graph_objects as go
import plotly_express as px
import dash
from dash import html, dcc, Input, Output

#leyendo los datos
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv',
                   encoding='ISO-8859-1',
                   dtype={'Div1Airport': str, 'Div1TailNum':str,
                          'Div2Airport': str, 'Div2TailNum':str})


#creando la aplicacion dash
app = dash.Dash(__name__)

#diseñando la aplicacion
app.layout = html.Div(children=[html.H1('Airline Performance Dashboard', style={'textAlign': 'center',
                                                              'color': '#503D36',
                                                              'font-size': 77}),
                                html.Div(['Input Year: ', dcc.Input(id='input-year',
                                                  value='2010',
                                                  type='number',
                                                  style={'height': '50px',
                                                         'font-size': '20'}),],style={'font-size': 40}),
                                html.Br(),
                                html.Br(),
                                html.Br(),
                                html.Div(dcc.Graph(id='line-plot')),
                                html.Div(html.H1('Total number of flights to the destination state split by reporting airline',
                                                 style={'textAlign':'center', 'color':'#503D36', 'font-size':40}),),
                                html.Div(dcc.Graph(id='bar-plot')),])
#agregando el decorador callback
@app.callback([Output(component_id='line-plot', component_property='figure'),
               Output(component_id='bar-plot', component_property='figure')],
              Input(component_id='input-year', component_property='value'))

#agregando la funcion de computo
def get_graph(year):
    #seleccionando los datos
    df = data[data['Year']==int(year)]
    #agrupando los datos por mes y calculando el promedio de tiempo de llegada
    line_data = df.groupby('Month')['ArrDelay'].mean().reset_index()
    bar_data = df.groupby('DestState')['Flights'].sum().reset_index()
    #figura
    fig = go.Figure(data = go.Scatter(x=line_data['Month'], y=line_data['ArrDelay'], mode='lines', marker=dict(color='green')))
    fig.update_layout(title='Month vs Average Flight Delay Time', xaxis_title='Month', yaxis_title='ArrDelay')
    fig2 = px.bar(bar_data, x='DestState', y='Flights', title='Total number of flights to te destination split by reporting airline')
    fig2.update_layout(title='Flights to Destination State', xaxis_title='DestState', yaxis_title='Flights')
    return fig, fig2


#ejecutar la aplicacion
if __name__ == '__main__':
    app.run_server()
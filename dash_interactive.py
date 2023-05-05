import pandas as pd
import dash
from dash import html, dcc, Input, Output
import plotly.express as px

# cargando los datos en un dataframe
data = pd.read_csv(
    'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv',
    encoding='ISO-8859-1',
    dtype={'Div1Airport': str, 'Div1TailNum': str,
           'Div2Airport': str, 'Div2TailNum': str})
# creando la aplicacion dash
app = dash.Dash(__name__)

# diseñando la aplicación
app.layout = html.Div(children=[html.H1('Flight Delay Time Statistics',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 30}),
                                html.Div(['Input Year: ', dcc.Input(id='input-year', value='2010',
                                                                    type='number',
                                                                    style={'height': '35px', 'fontsize': 30}), ],
                                         style={'font-size': 30}),
                                html.Br(),
                                html.Br(),
                                html.Br(),
                                # segmento 1
                                html.Div([
                                    html.Div(dcc.Graph(id='carrier-plot')),
                                    html.Div(dcc.Graph(id='weather-plot'))
                                ], style={'display': 'flex'}),
                                # segmento 2
                                html.Div([
                                    html.Div(dcc.Graph(id='nas-plot')),
                                    html.Div(dcc.Graph(id='security-plot'))
                                ], style={'display': 'flex'}),
                                # segmento 3
                                html.Div(dcc.Graph(id='late-plot'), style={'width': '100%'})
                                ])

""" Descripción de la función Compute_info
Esta función toma los datos de la línea aérea y el año seleccionado como entrada y realiza cálculos para crear gráficos y diagramas.
Argumentos:
    datos_línea_aérea: Datos de la línea aérea de entrada.
    año_introducido: Año de entrada para el que se debe realizar el cálculo.

Resultados:
    Promedio calculado de los marcos de datos para el retraso de la aerolínea, el retraso meteorológico, el retraso NAS, 
    el retraso de seguridad y el retraso de la aeronave."""


def compute_info(data, year):
    # selecionando la data
    df = data[data['Year'] == int(year)]
    # calculando la media de los retrasos
    avg_car = df.groupby(['Month', 'Reporting_Airline'])['CarrierDelay'].mean().reset_index()
    avg_weather = df.groupby(['Month', 'Reporting_Airline'])['WeatherDelay'].mean().reset_index()
    avg_NAS = df.groupby(['Month', 'Reporting_Airline'])['NASDelay'].mean().reset_index()
    avg_sec = df.groupby(['Month', 'Reporting_Airline'])['SecurityDelay'].mean().reset_index()
    avg_late = df.groupby(['Month', 'Reporting_Airline'])['LateAircraftDelay'].mean().reset_index()
    return avg_car, avg_weather, avg_NAS, avg_sec, avg_late


# callback decorador
'''funcion que devuelve figuras utilizando el año de entrada proporcionado
argumentos: año_introducido proporcionado por el usuario,
retorna:
lista de figuras calculadas utilizando la funcion 'compute_info'
'''


@app.callback([
    Output(component_id='carrier-plot', component_property='figure'),
    Output(component_id='weather-plot', component_property='figure'),
    Output(component_id='nas-plot', component_property='figure'),
    Output(component_id='security-plot', component_property='figure'),
    Output(component_id='late-plot', component_property='figure')
], Input(component_id='input-year', component_property='value'))
def get_graph(year):
    # información requerida para crear los graficos apartir de los datos
    avg_car, avg_weather, avg_NAS, avg_sec, avg_late = compute_info(data, year)
    # grafico de linea para el retardo de el equipaje
    carrier_fig = px.line(avg_car, x='Month', y='CarrierDelay', color='Reporting_Airline',
                          title='Average carrier delay time (minutes) by airline')
    # grafico de linea para el retardo por el clima
    weather_fig = px.line(avg_weather, x='Month', y='WeatherDelay', color='Reporting_Airline',
                          title='Average weather delay time (minutes) by airline')
    # grafico de linea para el retardo por nas
    nas_fig = px.line(avg_NAS, x='Month', y='NASDelay', color='Reporting_Airline',
                      title='Average NAS delay time(minutes) by airline')
    # grafico de linea para el retardo por seguridad
    sec_fig = px.line(avg_sec, x='Month', y='SecurityDelay', color='Reporting_Airline',
                      title='Average security delay time (minutes) by airline')
    # grafico de linea para el retardo por aeronaves
    late_fig = px.line(avg_late, x='Month', y='LateAircraftDelay', color='Reporting_Airline',
                       title='Average Late Aircraft delay (minutes) by airline')
    return [carrier_fig, weather_fig, nas_fig, sec_fig, late_fig]


if __name__ == '__main__':
    app.run_server()

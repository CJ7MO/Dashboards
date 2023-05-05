import pandas as pd
import dash
from dash import html, dcc, Input, Output, State
import plotly.express as px


#creando la app
app = dash.Dash(__name__)

#borrar el diseño y no mostrar la excepcion hasta que se ejecute la llamada de retorno (callback)
app.config.suppress_callback_exceptions = True
filename = 'filter_df.csv'
#cargando los datos
df = pd.read_csv(filename)


#diseñando la aplicacion
app.layout = html.Div(children=[html.H1('Car Automobile Components',
                                        style={'textAlign':'center', 'color':'#503D36',
                                               'font-size':27}),
    html.Div([
            html.Div(html.H2('Drive Wheels type: ', style={'margin-right': '2em'}),
            ),
            dcc.Dropdown(
                id='demo-dropdown',
                options=[
                    {'label': 'Real Wheel Drive', 'value': 'rwd'},
                    {'label': 'Front Wheel Drive', 'value': 'fwd'},
                    {'label': 'Four Wheel Drive', 'value': '4wd'}
                ],placeholder='select drive wheels',
                style={'width':'100%', 'padding':'3px', 'font-size': '20px', 'text-align-last' : 'center'},
            ),
            html.Div([
                html.Div([], id='plot1'),
                html.Div([], id='plot2')
            ], style={'display':'flex'}),
    ])
])

@app.callback([Output(component_id='plot1', component_property='children'),
               Output(component_id='plot2', component_property='children')],
               Input(component_id='demo-dropdown', component_property='value'),
              [State('plot1', 'children'),
               State('plot2', 'children')])

def display_selected_drive_charts(value, plot1, plot2):
    if value == 'rwd':
        rwd_df = df[df['drive-wheels']=='rwd'].groupby(['drive-wheels', 'body-style'], as_index=False).mean(numeric_only=True)
        rwd_df = rwd_df
        fig1 = px.pie(rwd_df, values='price', names='body-style', title='Pie Chart')
        fig2 = px.bar(rwd_df, x='body-style', y='price', color='body-style', title='Bar Chart')
        return [dcc.Graph(figure=fig1),
                dcc.Graph(figure=fig2)]
    if value == 'fwd':
        fwd_df = df[df['drive-wheels']=='fwd'].groupby(['drive-wheels', 'body-style'], as_index=False).mean(numeric_only=True)
        fwd_df = fwd_df
        fig1 = px.pie(fwd_df, values='price', names='body-style', title='Pie Chart')
        fig2 = px.bar(fwd_df, x='body-style', y='price', color='body-style', title='Bar Chart')
        return [dcc.Graph(figure=fig1),
                dcc.Graph(figure=fig2)]
    if value == '4wd':
        wd_df = df[df['drive-wheels'] == '4wd'].groupby(['drive-wheels', 'body-style'], as_index=False).mean(numeric_only=True)
        wd_df = wd_df
        fig1 = px.pie(wd_df, values='price', names='body-style', title='Pie Chart')
        fig2 = px.bar(wd_df, x='body-style', y='price', color='body-style', title='Bar Chart')
        return [dcc.Graph(figure=fig1),
                dcc.Graph(figure=fig2)]
    else:
        filter_df = df.groupby(['drive-wheels', 'body-style'], as_index=False).mean(numeric_only=True)
        filter_df = filter_df
        fig1 = px.pie(filter_df, values='price', names='body-style',color='body-style', title='Pie Chart')
        fig2 = px.bar(filter_df, x='body-style', y='price', color='body-style', title='Bar Chart')
        return [dcc.Graph(figure=fig1),
                dcc.Graph(figure=fig2)]

#ejecutar la aplicacion
if __name__ == '__main__':
    app.run_server(port='7777')

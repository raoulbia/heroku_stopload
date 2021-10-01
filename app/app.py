from flask import Flask
import pandas as pd
import dash_table
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State#, Event

server = Flask(__name__)

@server.route('/')
def hello_world():
    return 'Hello World!'

df = pd.read_csv('../assets/stopload_data.csv')
print(df.to_dict('records')[0])
print(df.columns)
columns = ['AtcoCode', 'PlateCode', 'Latitude', 'Longitude', 'StopLoadDay',
           'RoutesPassingThrough', 'RoutesPassingThroughCount',
           'OperatorsPassingThrough', 'OperatorsPassingThroughCount',
           'ShortCommonName_en', 'StopAccessibility', 'WheelchairAccessibility']
app = dash.Dash(__name__,
                server=server,
                routes_pathname_prefix='/dash/')

app.layout = dash_table.DataTable(id = "table",
                                  data=df.to_dict('records'),
                                  columns=[{'id': c, 'name': c} for c in df.columns],
                                  page_action='none',
                                  style_table={'height': '300px', 'overflowY': 'auto'},
                                    filter_action='native',

                                  )

# Table 1 left
@app.callback(
    Output('rel-dropdown-l', 'options'),
    [Input('subj-dropdown', 'value')])
def set_options_1_left(subject):
    if subject is None:
        return []
    else:
        df_aux = df_subj[df_subj['SUBJECT'] == subject]
        options = [{'label': i, 'value': i} for i in df_aux['RELATION'].unique().tolist()]
        return options

if __name__ == '__main__':
    app.run_server()
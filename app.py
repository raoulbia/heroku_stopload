# -*- coding: utf-8 -*-
import dash
import dash_table
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd

style_data_conditional = [
    {
        "if": {"state": "active"},
        "backgroundColor": "rgba(150, 180, 225, 0.2)",
        "border": "1px solid blue",
    },
    {
        "if": {"state": "selected"},
        "backgroundColor": "rgba(0, 116, 217, .03)",
        "border": "1px solid blue",
    },
]

layout_table = dict(
    autosize=True,
    height=500,
    font=dict(color="#191A1A"),
    titlefont=dict(color="#191A1A", size='14'),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=45
    ),
    hovermode="closest",
    plot_bgcolor='#fffcfc',
    paper_bgcolor='#fffcfc',
    legend=dict(font=dict(size=10), orientation='h'),
)

#####################
# Process Dataframe #
#####################

df = pd.read_csv('assets/stopload_data.csv',
                 encoding='Windows-1252',
                 # dtype=str
                 )
df = df.rename(columns={'StopLoadDay': 'NbrStopsPerDay'})
# print(df.columns)
df = df[['AtcoCode',
         'PlateCode',
         'ShortCommonName_en',
         'ShortCommonName_ga',
         'NbrStopsPerDay',
         'RoutesPassingThrough',
         'RoutesPassingThroughCount',
         'OperatorsPassingThrough',
         'OperatorsPassingThroughCount',
         'HasPole',
         'HasShelter',
         'CarouselType',
         'FlagData',
         'StopAccessibility',
         'WheelchairAccessibility',
         'isRTPI',
         'Latitude',
         'Longitude',
         # 'Image1',
         # 'Image2',
         # 'Image3',
         ]]

ls = []
for index, row in df.iterrows():
    rpt = row['RoutesPassingThrough'].split(', ')
    rpt = [i.replace(' ', '') for i in rpt]
    for i in rpt:
        ls.append(i)
ls = sorted(list(set(ls)))
# print(len(ls))
# print(ls[:5])

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets,
                )
# app.scripts.config.serve_locally = True
app.css.config.serve_locally = True
server = app.server
app.title = 'Stop Explorer'
app.layout = html.Div(
    children=[

    html.H1(children='Stop Explorer', style={'textAlign': 'center',
                                             # 'font-size': '28px',
                                             'background-image': 'url(https://www.transportforireland.ie/wp-content/themes/transportforireland/assets/img/branding/transport-for-ireland-logo.svg)',
                                             'background-position': 'left',
                                             'background-repeat': 'no-repeat'}) ,
    html.P('''
            Search for Bus Stops served by one or more routes. 
            When selecting multiple routes, the application will show stops that
            are served by either route. 
            To see stops that are shared check the tick box. 
           ''', style={'textAlign': 'left',
                       'marginLeft': 150,
                       'marginRight': 100,
                       'marginBottom': 50}),

    # Row 0
    # html.Div(
    #     [
    #         # Subject left drop down
    #         html.Div(
    #             [
    #                 html.H3(''),
    #             ], className='six columns'
    #         ),
    #     ], className='row'),


    # Row 1

    html.Div([
            # Subject left drop down

        html.Div(
            ['Routes: '],
                 className='one columns',
                 style={"margin": 0}
                 ),

        html.Div(
            [
                dcc.Dropdown(
                    id='routes-dropdown',
                    placeholder='Select Route(s)...',
                    multi=True,
                    options=[{'label': item, 'value': item} for item in ls]),

            ], style={'marginBottom': 10, 'marginLeft':10},
                className='three columns'),

        # shared checkbox
        html.Div(
            [
                    dcc.Checklist(
                        id='shared-stop',
                        options=[
                            {'label': 'shared', 'value': 'true'},
                        ],
                        value=[],
                        # style={'display': 'inline-block',
                        #        'position': 'absolute',
                        #        'top':'90px',
                        #        'left':'550px'}
                    ),

                ], className='two columns'),

        ], className='row'),

    html.Div(
        [
            dash_table.DataTable(
                css=[{'selector': '.export',
                      # 'rule':'position: relative;top:-20px;left:1050px;'
                      'rule': 'position: absolute;top:-10%;right: 0;width: 120px;'
                      # 'rule':'display: flex;align-items: center;justify-content: space-between;'
                      }],
                id='datatable',
                columns=[{'id': c, 'name': c} for c in df.columns],
                data=df.to_dict('records'),
                fixed_rows={'headers': True, 'data': 0},
                export_format="csv",
                export_headers="display",
                # row_selectable='single',
                # style_data_conditional=style_data_conditional,
                # selected_rows=[],
                sort_action='native',
                # filter_action='native',
                style_table={'height': '500px',
                             'overflowY': 'auto'},
                style_cell={'padding': '10px', 'textAlign': 'left'},
                style_data={'width': '150px',
                            'minWidth': '150px',
                            # 'maxWidth': '150px',
                            # 'overflow': 'hidden',
                            'textOverflow': 'ellipsis', }
            )
        ], style=layout_table),

    ], className='ten columns offset-by-one'

) # end main Div


#############
# Callbacks #
#############

@app.callback(
    Output("datatable", "data"),
    [
        Input('routes-dropdown', 'value'),
        Input('shared-stop', 'value'),
        # Input('rel-dropdown-l', 'value')
     ])
def update_datatable(x, y):
    print(y)
    try:
        kw = [i for i in x]
    except:
        kw = []

    if x is None or kw == []:
        return df.to_dict('records')
    else:

        tmp = df.copy()
        tmp['rpt'] = tmp['RoutesPassingThrough'].apply(lambda x: x.split(', '))
        tmp['rpt'] = tmp['rpt'].apply(lambda x: [i.replace(' ', '') for i in x])
        # print(kw)

        if y:
            tmp['match'] = (tmp.rpt.apply(lambda x: 1 if all([k in x for k in kw]) else 0))
        else:
            tmp['match'] = (tmp.rpt.apply(lambda x: 1 if any([k in x for k in kw]) else 0))
        # print(tmp.head())
        tmp = tmp[tmp['match'] == 1]
        tmp = tmp.drop(['match', 'rpt'], 1)


    # selected_rows = tmp.to_dict('records')
    return tmp.to_dict('records')

# @app.callback(
#     Output("datatable", "style_data_conditional"),
#     [Input("datatable", "active_cell")]
# )
# def update_selected_row_color(active):
#     print(active)
#     style = style_data_conditional.copy()
#     if active:
#         style.append(
#             {
#                 "if": {"row_index": active["row"]},
#                 "backgroundColor": "rgba(150, 180, 225, 0.2)",
#                 "border": "1px solid blue",
#             },
#         )
#     if active is None:
#         style = None
#     return style


if __name__ == '__main__':
    # app.run_server(debug=True)
    app.server.run(debug=True, threaded=True)

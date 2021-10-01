# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import dash_table
from dash.dependencies import Input, Output, State#, Event
import pandas as pd
import collections



df = pd.read_csv('../assets/SEMMEDDB_TRIPLES_FINAL.csv')

# DFs for PART 1
df_subj = df.copy()
df_subj = df_subj[df_subj['IS_MASTER_GENE']=='subject']
df_subj = df_subj[['SUBJECT', 'RELATION', 'OBJECT', 'PMID']].copy()
df_subj['PMID'] = df_subj['PMID'].apply(lambda x: x.split(','))
df_subj['PMID_Count'] = df_subj['PMID'].apply(lambda x: len(x))
df_subj = df_subj[['SUBJECT', 'RELATION', 'OBJECT', 'PMID_Count']]#, 'PMID']]
items_subj = sorted(df_subj['SUBJECT'].unique().tolist())

df_obj = df.copy()
df_obj = df_obj[df_obj['IS_MASTER_GENE']=='object']
df_obj = df_obj[['SUBJECT', 'RELATION', 'OBJECT', 'PMID']].copy()
df_obj['PMID'] = df_obj['PMID'].apply(lambda x: x.split(','))
df_obj['PMID_Count'] = df_obj['PMID'].apply(lambda x: len(x))
df_obj = df_obj[['SUBJECT', 'RELATION', 'OBJECT', 'PMID_Count']]#, 'PMID']]
items_obj = sorted(df_obj['OBJECT'].unique().tolist())


# DFs for PART 2
df_subj2 = df.copy()
df_subj2 = df_subj2[df_subj2['IS_MASTER_GENE']=='subject']
df_subj2 = df_subj2[['SUBJECT', 'RELATION', 'OBJECT', 'PMID']]
df_subj2['PMID'] = df_subj2['PMID'].apply(lambda x: len(x.split(',')))
grouped = df_subj2.groupby(['RELATION', 'OBJECT']).agg({'SUBJECT': ['count'], 'PMID': ['sum']})
df_subj2 = pd.DataFrame((grouped.reset_index()))
df_subj2.columns=(['RELATION', 'OBJECT', 'Subject_Count', 'PMID_Count'])
df_subj2_rels = sorted(df_subj2['RELATION'].unique().tolist())

df_obj2 = df.copy()
df_obj2 = df_obj2[df_obj2['IS_MASTER_GENE']=='object']
df_obj2 = df_obj2[['SUBJECT', 'RELATION', 'OBJECT', 'PMID']]
df_obj2['PMID'] = df_obj2['PMID'].apply(lambda x: len(x.split(',')))
grouped = df_obj2.groupby(['RELATION', 'SUBJECT']).agg({'OBJECT': ['count'], 'PMID': ['sum']})
df_obj2 = pd.DataFrame((grouped.reset_index()))
df_obj2.columns=(['RELATION', 'SUBJECT', 'Object_Count', 'PMID_Count']) # rename
df_obj2_rels = sorted(df_obj2['RELATION'].unique().tolist())


# DFs for PART 3
df_subj3 = df.copy()
df_subj3 = df_subj3[df_subj3['IS_MASTER_GENE']=='subject']
df_subj3 = df_subj3[['SUBJECT', 'RELATION', 'OBJECT', 'PMID']].copy()
df_subj3['PMID_Count'] = df_subj3['PMID'].apply(lambda x: len(x.split(',')))
df_subj3['PMID'] = df_subj3['PMID'].apply(lambda x: x.split('\,'))
df_subj3 = df_subj3[['SUBJECT', 'RELATION', 'OBJECT', 'PMID_Count', 'PMID']]
items_rels31 = sorted(df_subj3['RELATION'].unique().tolist())
items_subj3 = sorted(df_subj3['SUBJECT'].unique().tolist())

df_obj3 = df.copy()
df_obj3 = df_obj3[df_obj3['IS_MASTER_GENE']=='object']
df_obj3 = df_obj3[['SUBJECT', 'RELATION', 'OBJECT', 'PMID']].copy()
df_obj3['PMID_Count'] = df_obj3['PMID'].apply(lambda x: len(x.split(',')))
df_obj3['PMID'] = df_obj3['PMID'].apply(lambda x: x.split('\,'))
df_obj3 = df_obj3[['SUBJECT', 'RELATION', 'OBJECT', 'PMID_Count', 'PMID']]
items_rels32 = sorted(df_obj3['RELATION'].unique().tolist())
items_obj3 = sorted(df_obj3['OBJECT'].unique().tolist())


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.scripts.config.serve_locally = False
server = app.server
app.title = 'SemmedDB Triple Explorer'

 # Layouts
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

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}


app.layout = html.Div(children=[

    html.H1('SemmedDB Triple Explorer', style={'textAlign': 'center'}),
    html.P('''
            The Semantic MEDLINE Database (SemMedDB) is a repository of semantic predications (subject-predicate-object df) extracted
            from approx. 29.7M PubMed citations.
           '''),


##########
# PART 1 #
##########

    # Row 0
    html.Div(
        [
        # Subject left drop down
        html.Div(
            [
            html.H3('Subject View'),
            ], className='six columns'),

        # Object right drop down
        # html.Div(
        #     [
        #     html.H3('Object View'),
        #     ], className='six columns'),
        ], className='row'),

    # Row 1
    html.Div(
        [
        # Subject left drop down
        html.Div(
            [
                html.Div('Subject', className='three columns'),
                html.Div(
                    [
                    dcc.Dropdown(
                    id='subj-dropdown',
                    options= [{'label': item, 'value': item} for item in items_subj])
                    ], className='four columns'),
            ], className='six columns'),
        ], className='row'),

    # # Row 2
    # html.Div(
    #     [
    #         # Relation left  drop down
    #         html.Div(
    #             [
    #                 html.Div('Relation', className='three columns'),
    #                 html.Div(
    #                     [
    #                     dcc.Dropdown(id='rel-dropdown-l')
    #                     ], className='four columns'),
    #             ], className='six columns'),
    #
    #         # Relation right drop down
    #         html.Div(
    #             [
    #                 html.Div('Relation', className='three columns'),
    #                 html.Div(
    #                     [
    #                     dcc.Dropdown(id='rel-dropdown-r')
    #                     ], className='four columns'),
    #             ], className='six columns'),
    #     ], className='row'),

    # Row 3
    html.Div(
        [
        # Table 1
        html.Div(
            [
                # dash_table.DataTable(
                #     id = 'datatable-1-l',
                #     columns=[{'id': c, 'name': c} for c in df_subj.columns],
                #         assets=df_subj.to_dict('records'),
                #         selected_rows=[],
                #     style_table={'height': '300px', 'overflowY': 'auto'},
                #         style_data={
                #             'width': '150px', 'minWidth': '150px', 'maxWidth': '150px',
                #             'overflow': 'hidden',
                #             'textOverflow': 'ellipsis',
                #         }
                #     )
            ],
            style = layout_table ,
            className='six columns'),

        # Table 2
        # html.Div(
        #     [
        #     ], style = layout_table, className='six columns'),
        ]
        , className='row'),


], className='ten columns offset-by-one') # end main Div


####################
# Callbacks PART 1 #
####################

# Table 1 left
# @app.callback(
#     Output('rel-dropdown-l', 'options'),
#     [Input('subj-dropdown', 'value')])
# def set_options_1_left(subject):
#     if subject is None:
#         return []
#     else:
#         df_aux = df_subj[df_subj['SUBJECT'] == subject]
#         options = [{'label': i, 'value': i} for i in df_aux['RELATION'].unique().tolist()]
#         return options


# @app.callback(
#     Output('datatable-1-l', 'selected_rows'),
#     [
#         Input('subj-dropdown', 'value'),
#         # Input('rel-dropdown-l', 'value')
#      ])
# def update_datatable_1_left(x, y):
#     if x is None and y is None:
#         df_aux = df_subj
#     elif not x is None and y is None:
#         df_aux = df_subj[df_subj['SUBJECT'] == x]
#     elif x is None and not y is None:
#         df_aux = df_subj[df_subj['RELATION'] == y]
#     else:
#         df_aux = df_subj[(df_subj['SUBJECT'] == x) & (df_subj['RELATION'] == y)]
#
#     df_aux = df_aux.sort_values(by='PMID_Count', ascending=False)
#     selected_rows = df_aux.to_dict('records')
#     return selected_rows




if __name__ == '__main__':
    # app.run_server()
    app.server.run(debug=True, threaded=True)
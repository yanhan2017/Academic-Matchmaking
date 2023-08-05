from dash import html, dcc, Input, Output, callback, dash_table, ctx


def create_widget_five(graphdb):
    all_faculty_list = graphdb.get_all_faculty()

    @callback(
        Output(component_id='fav_faculty_table', component_property='data'),
        Input(component_id='add_input', component_property='value'),
        Input(component_id='delete_input', component_property='value'),
    )
    def get_fav_faculty_table(add_faculty, delete_faculty):
        update_fav_faculty(add_faculty, delete_faculty)
        return graphdb.get_all_fav_faculty().to_dict('records')

    @callback(
        Output(component_id='delete_input', component_property='options'),
        Input(component_id='add_input', component_property='value'),
        Input(component_id='delete_input', component_property='value'),
    )
    def get_fav_faculty_list(add_faculty, delete_faculty):
        update_fav_faculty(add_faculty, delete_faculty)
        return graphdb.get_all_fav_faculty(to_list=True)

    def update_fav_faculty(add_faculty, delete_faculty):
        triggered_id = ctx.triggered_id
        if add_faculty is not None and triggered_id == 'add_input':
            graphdb.add_fav_faculty(add_faculty)
        elif delete_faculty is not None and triggered_id == 'delete_input':
            graphdb.delete_fav_faculty(delete_faculty)

    return html.Div(children=[
        html.Label('Add favorite faculty'),
        dcc.Dropdown(all_faculty_list, id='add_input'),
        html.Br(),
        html.Label('Delete favorite faculty'),
        dcc.Dropdown(id='delete_input'),
        html.Br(),
        dash_table.DataTable(columns=[{"name": "Faculty Name", "id": "n.name"}],
                             id='fav_faculty_table')
    ], style={"height": "100%", "width": "20%"})


def create_widget_six(graphdb):
    all_faculty_list = graphdb.get_all_faculty()

    @callback(
        Output(component_id='graph_output', component_property='children'),
        Input(component_id='advisor_input', component_property='value')
    )
    def create_visual_graph(advisor_input):
        if advisor_input is None:
            return html.Div("Choose your advisor to display graph")
        return html.Iframe(srcDoc=graphdb.get_co_author_graph(advisor_input).html,
                           style={"height": "100%", "width": "100%", "border": "none"})

    return html.Div(children=[
                        html.Label('Choose your advisor'),
                        dcc.Dropdown(all_faculty_list, id='advisor_input'),
                        html.Br(),
                        html.Label('Co-authorship graph'),
                        html.Div(id='graph_output', style={"height": "100%", "width": "100%"})],
                    style={"position": "absolute", "left": "25%", "top": "0.5%", "height": "100%", "width": "80%"})

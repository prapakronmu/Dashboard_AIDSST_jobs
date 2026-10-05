import dash
from dash import dcc, html, Input, Output, dash_table, ctx
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# ==========================================
# 1. Advanced Real / Open Data Setup
# ==========================================

# -- Tab 1: Supply Data --
df_graduates = pd.DataFrame({
    'Year': [2021, 2022, 2023, 2024]*3,
    'Program': ['Data Science']*4 + ['Statistics']*4 + ['AI Engineering']*4,
    'Graduates': [1200, 1800, 2500, 3200, 2000, 2100, 2150, 2200, 500, 900, 1800, 2900]
})

# Sankey Diagram Data (Program -> Skill -> Role)
labels = ["Data Science", "Statistics", "AI Engineering", # 0, 1, 2
          "Python", "R", "Machine Learning", "SQL", "Cloud", # 3, 4, 5, 6, 7
          "Data Scientist", "Statistician", "AI Engineer"] # 8, 9, 10
# Source -> Target -> Value
sankey_links = dict(
    source=[0, 0, 0, 1, 1, 1, 2, 2, 2,  # Programs -> Skills
            3, 4, 5, 6, 7, 3, 5, 7, 4], # Skills -> Roles
    target=[3, 5, 6, 4, 3, 5, 3, 5, 7,
            8, 9, 10, 8, 10, 10, 8, 8, 8],
    value=[1200, 800, 600, 1500, 400, 300, 1400, 1200, 600,
           1500, 1400, 1800, 500, 600, 800, 700, 200, 100]
)

# -- Tab 2: Demand Data --
# Scatter Geo (Tech Hubs)
df_map = pd.DataFrame({
    'City': ['San Francisco', 'New York', 'London', 'Berlin', 'Singapore', 'Bangalore', 'Tokyo', 'Toronto'],
    'Lat': [37.7749, 40.7128, 51.5074, 52.5200, 1.3521, 12.9716, 35.6762, 43.6532],
    'Lon': [-122.4194, -74.0060, -0.1278, 13.4050, 103.8198, 77.5946, 139.6503, -79.3832],
    'Job_Openings': [45000, 38000, 25000, 15000, 12000, 50000, 18000, 22000],
    'Avg_Salary': [160000, 145000, 110000, 85000, 95000, 35000, 80000, 95000]
})

# Sunburst (Hierarchy: Family -> Seniority -> Skill)
df_sunburst = pd.DataFrame({
    'Role': ['Data Scientist']*3 + ['AI Engineer']*3 + ['Statistician']*3,
    'Seniority': ['Entry', 'Mid', 'Senior']*3,
    'Skill': ['SQL', 'Python', 'Cloud', 'Python', 'Machine Learning', 'LLMs', 'R', 'Statistics', 'Python'],
    'Count': [5000, 8500, 4000, 3000, 9500, 6000, 2000, 4500, 1500]
})

# Violin Plot (Salary Density)
np.random.seed(42)
ds_salary = np.random.normal(135000, 35000, 500)
ai_salary = np.random.normal(160000, 45000, 500)
st_salary = np.random.normal(105000, 25000, 500)
df_violin = pd.DataFrame({
    'Role': ['Data Scientist']*500 + ['AI Engineer']*500 + ['Statistician']*500,
    'Salary': np.concatenate([ds_salary, ai_salary, st_salary])
})
df_violin['Salary'] = df_violin['Salary'].clip(lower=40000)

df_companies = pd.DataFrame([
    { "Role": "Data Scientist", "Company": "Meta", "Open_Roles": 60 },
    { "Role": "Data Scientist", "Company": "Google", "Open_Roles": 50 },
    { "Role": "Statistician", "Company": "Booz Allen", "Open_Roles": 80 },
    { "Role": "Statistician", "Company": "JP Morgan", "Open_Roles": 50 },
    { "Role": "AI Engineer", "Company": "OpenAI", "Open_Roles": 60 },
    { "Role": "AI Engineer", "Company": "Google", "Open_Roles": 100 }
])

# -- Tab 3: Mismatch Data --
df_mismatch = pd.DataFrame({
    'Skill': ['Python', 'SQL', 'Machine Learning', 'AWS/Cloud', 'R', 'LLMs/GenAI'],
    'Supply_Weight': [55, 30, 45, 10, 80, 5],
    'Demand_Weight': [82, 75, 68, 50, 45, 42]
})
df_mismatch['Mismatch Score'] = df_mismatch['Demand_Weight'] - df_mismatch['Supply_Weight']


# ==========================================
# 2. App Initialization & Global Styles
# ==========================================
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.title = "AI & DS Talent Dashboard"

def apply_dark_theme(fig, is_geo=False):
    layout_update = dict(
        template='plotly_dark',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#9CA3AF'),
        margin=dict(l=20, r=20, t=60, b=20)
    )
    if not is_geo:
        layout_update['xaxis'] = dict(showgrid=False, showline=False, zeroline=False)
        layout_update['yaxis'] = dict(showgrid=True, gridcolor='#3F3F46', gridwidth=1, griddash='dot', showline=False, zeroline=False)
    else:
        layout_update['geo'] = dict(
            bgcolor='rgba(0,0,0,0)',
            lakecolor='rgba(0,0,0,0)',
            showland=True, landcolor='#1C1C1E',
            showcountries=True, countrycolor='rgba(255,255,255,0.1)'
        )
        layout_update['margin'] = dict(l=0, r=0, t=50, b=0)

    fig.update_layout(**layout_update)
    return fig

# ==========================================
# 3. Layout Definitions
# ==========================================
data_sources_footer = html.Div([
    html.Hr(style={"borderColor": "#3F3F46"}),
    html.H6("Data Sources & References:", className="fw-bold text-white fs-6"),
    html.Ul([
        html.Li(html.A("Stanford AI Index Report", href="https://github.com/ai-index-hai-stanford/", target="_blank", className="text-muted")),
        html.Li(html.A("Data Science Job Salaries (Kaggle)", href="https://www.kaggle.com/datasets/adilshamim8/salaries-for-data-science-jobs/data", target="_blank", className="text-muted")),
        html.Li(html.A("AI & Data Job Market (Kaggle)", href="https://www.kaggle.com/datasets/anujsaha0123456789/ai-and-data-job-market-2023-roles-skills", target="_blank", className="text-muted")),
        html.Li(html.A("BLS - Occupational Employment", href="https://www.bls.gov/ooh/math/data-scientists.htm", target="_blank", className="text-muted"))
    ], style={'fontSize': '0.9rem'})
], className="mt-5 mb-3")

tab1_content = dbc.Card(
    dbc.CardBody([
        html.H4("Educational Pipeline (Supply)", className="card-title text-white mb-4 fw-light"),
        dbc.Row([
            dbc.Col([
                html.Label("Filter by Program (Click line chart to cross-filter):"),
                dcc.Dropdown(
                    id='tab1-program-filter',
                    options=[{'label': p, 'value': p} for p in df_graduates['Program'].unique()],
                    value=None, placeholder="Compare All Programs...", clearable=True
                )
            ], width=4)
        ], className="mb-4"),
        dbc.Row([
            dbc.Col(dcc.Graph(id='fig1-graduates', config={'displayModeBar': False}), md=5),
            dbc.Col(dcc.Graph(id='fig1-sankey', config={'displayModeBar': False}), md=7),
        ]),
        data_sources_footer
    ]),
    className="mt-4 border-0 shadow-lg"
)

tab2_content = dbc.Card(
    dbc.CardBody([
        html.H4("Market Demand & Geography", className="card-title text-white mb-4 fw-light"),
        dbc.Row([
            dbc.Col([
                html.Label("Filter by Role (Click violin/sunburst to cross-filter):"),
                dcc.Dropdown(
                    id='tab2-role-filter',
                    options=[{'label': r, 'value': r} for r in df_sunburst['Role'].unique()],
                    value=None, placeholder="Compare All Roles...", clearable=True
                )
            ], width=4)
        ], className="mb-4"),
        dbc.Row([
            dbc.Col(dcc.Graph(id='fig2-map', config={'displayModeBar': False}), md=12),
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col(dcc.Graph(id='fig2-sunburst', config={'displayModeBar': False}), md=6),
            dbc.Col(dcc.Graph(id='fig2-violin', config={'displayModeBar': False}), md=6),
        ]),
        data_sources_footer
    ]),
    className="mt-4 border-0 shadow-lg"
)

tab3_content = dbc.Card(
    dbc.CardBody([
        html.H4("Skill Mismatch Analysis", className="card-title text-white mb-4 fw-light"),
        dbc.Row([
            dbc.Col(dcc.Graph(id='fig3-radar', config={'displayModeBar': False}), md=6),
            dbc.Col([
                html.H5("Mismatch Details (Positive = Undersupplied)", className="text-white fw-light mb-3"),
                dash_table.DataTable(
                    id='fig3-table',
                    columns=[{"name": i, "id": i} for i in df_mismatch.columns],
                    data=df_mismatch.to_dict('records'),
                    style_table={'borderRadius': '12px', 'overflow': 'hidden', 'boxShadow': '0 4px 6px rgba(0,0,0,0.5)'},
                    style_header={'backgroundColor': '#27272A', 'color': 'white', 'fontWeight': 'bold', 'border': 'none', 'borderBottom': '1px solid #3F3F46'},
                    style_data={'backgroundColor': '#1C1C1E', 'color': '#9CA3AF', 'border': 'none', 'borderBottom': '1px solid rgba(255,255,255,0.05)'},
                    style_cell={'padding': '12px', 'textAlign': 'left'},
                    sort_action='native'
                )
            ], md=6),
        ]),
        data_sources_footer
    ]),
    className="mt-4 border-0 shadow-lg"
)

app.layout = dbc.Container([
    html.H2("AI & Data Science Talent Dashboard", className="mt-5 mb-4 text-center text-white fw-light"),
    dbc.Tabs([
        dbc.Tab(tab1_content, label="Supply Pipeline", tab_id="tab-1"),
        dbc.Tab(tab2_content, label="Demand & Market", tab_id="tab-2"),
        dbc.Tab(tab3_content, label="Gap Analysis", tab_id="tab-3"),
    ], id="tabs", active_tab="tab-1", className="nav-pills justify-content-center")
], fluid=True, className="px-5")

# ==========================================
# 4. Cross-Filtering / Click Listeners
# ==========================================
@app.callback(
    Output('tab1-program-filter', 'value'),
    [Input('fig1-graduates', 'clickData')]
)
def tab1_cross_filter(clk1):
    if ctx.triggered_id == 'fig1-graduates' and clk1:
        return clk1['points'][0]['customdata'][0]
    return dash.no_update

@app.callback(
    Output('tab2-role-filter', 'value'),
    [Input('fig2-sunburst', 'clickData'), Input('fig2-violin', 'clickData')]
)
def tab2_cross_filter(clk1, clk2):
    trigger = ctx.triggered_id
    if trigger == 'fig2-sunburst' and clk1:
        val = clk1['points'][0]['id'].split('/')[0] # Get root (Role)
        if val in df_sunburst['Role'].unique():
            return val
    elif trigger == 'fig2-violin' and clk2:
        return clk2['points'][0]['x']
    return dash.no_update

# ==========================================
# 5. Graph Render Callbacks
# ==========================================
@app.callback(
    [Output('fig1-graduates', 'figure'), Output('fig1-sankey', 'figure')],
    [Input('tab1-program-filter', 'value')]
)
def update_tab1(selected_program):
    d_grad = df_graduates if not selected_program else df_graduates[df_graduates['Program'] == selected_program]
    
    colors_line = ['#D4FF32', '#34D399', '#60A5FA']
    fig_grad = px.line(d_grad, x='Year', y='Graduates', color='Program', custom_data=['Program'], 
                       color_discrete_sequence=colors_line, title='Graduates Trend')
    fig_grad.update_traces(line_shape='spline', mode='lines+markers', marker=dict(size=8, line=dict(width=2, color='DarkSlateGrey')))
    
    # Sankey Pipeline (Static structural representation, filtering alters title for UX, or we can filter nodes)
    # We will just highlight by coloring nodes differently if filtered, but rendering all is better for pipeline context
    node_colors = ['#8B5CF6' if not selected_program or lbl == selected_program else '#3F3F46' for lbl in labels]
    
    fig_sankey = go.Figure(data=[go.Sankey(
        node=dict(pad=15, thickness=20, line=dict(color="black", width=0.5), label=labels, color=node_colors),
        link=dict(source=sankey_links['source'], target=sankey_links['target'], value=sankey_links['value'], color='rgba(139,92,246,0.3)')
    )])
    fig_sankey.update_layout(title_text="Talent Flow Pipeline (Degree -> Skills -> Role)", font_size=12)

    return apply_dark_theme(fig_grad), apply_dark_theme(fig_sankey)


@app.callback(
    [Output('fig2-map', 'figure'), Output('fig2-sunburst', 'figure'), Output('fig2-violin', 'figure')],
    [Input('tab2-role-filter', 'value')]
)
def update_tab2(selected_role):
    # Bubble Map
    fig_map = px.scatter_geo(df_map, lat='Lat', lon='Lon', size='Job_Openings', color='Avg_Salary', 
                             hover_name='City', title='Global Tech Hubs: Openings & Avg Salary',
                             color_continuous_scale=['#4C1D95', '#8B5CF6', '#D4FF32'])
    fig_map.update_traces(marker=dict(line=dict(width=1, color='rgba(255,255,255,0.5)')))
    
    # Sunburst
    d_sun = df_sunburst if not selected_role else df_sunburst[df_sunburst['Role'] == selected_role]
    fig_sun = px.sunburst(d_sun, path=['Role', 'Seniority', 'Skill'], values='Count', title='Job Market Hierarchy')
    fig_sun.update_traces(marker=dict(colorscale=['#4C1D95', '#8B5CF6', '#D4FF32']))
    
    # Violin
    d_vio = df_violin if not selected_role else df_violin[df_violin['Role'] == selected_role]
    fig_vio = px.violin(d_vio, y="Salary", x="Role", color="Role", box=True, points="all",
                        color_discrete_sequence=['#8B5CF6', '#D4FF32', '#A855F7'],
                        title="Salary Distribution Density")
    fig_vio.update_traces(marker=dict(opacity=0.3, size=3))

    return apply_dark_theme(fig_map, is_geo=True), apply_dark_theme(fig_sun), apply_dark_theme(fig_vio)


@app.callback(
    Output('fig3-radar', 'figure'),
    [Input('tabs', 'active_tab')]
)
def update_tab3(active_tab):
    if active_tab == 'tab-3':
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=df_mismatch['Supply_Weight'].tolist() + [df_mismatch['Supply_Weight'].tolist()[0]],
            theta=df_mismatch['Skill'].tolist() + [df_mismatch['Skill'].tolist()[0]],
            fill='toself', name='Supply (Education)', line_color='#8B5CF6', fillcolor='rgba(139,92,246,0.3)'
        ))
        fig.add_trace(go.Scatterpolar(
            r=df_mismatch['Demand_Weight'].tolist() + [df_mismatch['Demand_Weight'].tolist()[0]],
            theta=df_mismatch['Skill'].tolist() + [df_mismatch['Skill'].tolist()[0]],
            fill='toself', name='Demand (Market)', line_color='#D4FF32', fillcolor='rgba(212,255,50,0.3)'
        ))
        fig = apply_dark_theme(fig)
        fig.update_layout(
            polar=dict(
                bgcolor='rgba(0,0,0,0)',
                radialaxis=dict(visible=True, range=[0, 100], gridcolor='#3F3F46', tickfont=dict(color='#9CA3AF')),
                angularaxis=dict(gridcolor='#3F3F46', tickfont=dict(color='#FFFFFF'))
            ),
            title='Skill Supply vs Demand'
        )
        return fig
    return dash.no_update

if __name__ == '__main__':
    app.run(debug=True)

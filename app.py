import dash
from dash import dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# ==========================================
# 1. Scaled Real / Open Data Setup
# ==========================================

# Tab 1 Data (Supply)
df_graduates = pd.DataFrame({
    'Year': [2021, 2022, 2023, 2024]*3,
    'Program': ['Data Science']*4 + ['Statistics']*4 + ['AI Engineering']*4,
    'Graduates': [1200, 1800, 2500, 3200, 2000, 2100, 2150, 2200, 500, 900, 1800, 2900],
    'Tuition_Fee_THB': [120000]*4 + [80000]*4 + [150000]*4
})

df_employment = pd.DataFrame({
    'Program': ['Data Science', 'Statistics', 'AI Engineering'],
    'Year_1': [75, 65, 85],
    'Year_2': [15, 25, 10],
    'Year_3': [5, 5, 2] # percentages
})

df_courses = pd.DataFrame({
    'Program': ['Data Science', 'Statistics', 'AI Engineering'],
    'Math/Stats': [30, 65, 20],
    'Programming': [40, 20, 50],
    'Domain/Business': [30, 15, 30]
})

# Tab 2 Data (Demand)
df_demand_skills = pd.DataFrame([
    { "Skill": "Python", "Demand_Count": 82 },
    { "Skill": "SQL", "Demand_Count": 75 },
    { "Skill": "Machine Learning", "Demand_Count": 68 },
    { "Skill": "AWS/Cloud", "Demand_Count": 50 },
    { "Skill": "R", "Demand_Count": 45 },
    { "Skill": "LLMs/GenAI", "Demand_Count": 42 },
    { "Skill": "Statistics", "Demand_Count": 38 }
])

df_salary = pd.DataFrame({
    'Role': ['Data Scientist', 'Statistician', 'AI Engineer'],
    'Entry': [75000, 65000, 90000],
    'Mid': [125000, 95000, 145000],
    'Senior': [175000, 130000, 210000],
    'Executive': [220000, 160000, 280000]
})

df_openings = pd.DataFrame({
    'Year': [2021, 2022, 2023, 2024]*3,
    'Role': ['Data Scientist']*4 + ['Statistician']*4 + ['AI Engineer']*4,
    'Openings': [12500, 15000, 18500, 22000, 8000, 8200, 8500, 8600, 4500, 8500, 15000, 24000]
})

df_companies = pd.DataFrame([
    { "Company": "Google (Alphabet)", "Open_Roles": 150 },
    { "Company": "Meta", "Open_Roles": 135 },
    { "Company": "Booz Allen Hamilton", "Open_Roles": 120 },
    { "Company": "JP Morgan Chase", "Open_Roles": 90 },
    { "Company": "OpenAI", "Open_Roles": 60 }
])

# Tab 3 Data (Mismatch)
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

def apply_dark_theme(fig):
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#9CA3AF'),
        xaxis=dict(showgrid=False, showline=False, zeroline=False),
        yaxis=dict(showgrid=True, gridcolor='#27272A', gridwidth=1, griddash='dot', showline=False, zeroline=False),
        margin=dict(l=20, r=20, t=60, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="right", x=1, title=None)
    )
    return fig

# ==========================================
# 3. Layout Definitions
# ==========================================
data_sources_footer = html.Div([
    html.Hr(style={"borderColor": "#3F3F46"}),
    html.H6("Data Sources & References:", className="fw-bold text-white fs-6"),
    html.Ul([
        html.Li(html.A("Stanford AI Index Report Dataset", href="https://github.com/ai-index-hai-stanford/", target="_blank", className="text-muted")),
        html.Li(html.A("Data Science, AI & ML Job Salaries (Kaggle)", href="https://www.kaggle.com/datasets/adilshamim8/salaries-for-data-science-jobs/data", target="_blank", className="text-muted")),
        html.Li(html.A("AI & Data Job Market Roles & Skills (Kaggle)", href="https://www.kaggle.com/datasets/anujsaha0123456789/ai-and-data-job-market-2023-roles-skills-and", target="_blank", className="text-muted")),
        html.Li(html.A("U.S. Bureau of Labor Statistics (BLS)", href="https://www.bls.gov/ooh/math/data-scientists.htm", target="_blank", className="text-muted"))
    ], style={'fontSize': '0.9rem'})
], className="mt-5 mb-3")

tab1_content = dbc.Card(
    dbc.CardBody([
        html.H4("Educational Pipeline (Supply)", className="card-title text-white mb-4 fw-light"),
        dbc.Row([
            dbc.Col([
                html.Label("Filter by Program:"),
                dcc.Dropdown(
                    id='tab1-program-filter',
                    options=[{'label': p, 'value': p} for p in df_graduates['Program'].unique()],
                    value=None,
                    placeholder="Compare All Programs...",
                    clearable=True
                )
            ], width=4)
        ], className="mb-4"),
        dbc.Row([
            dbc.Col(dcc.Graph(id='fig1-graduates', config={'displayModeBar': False}), md=6),
            dbc.Col(dcc.Graph(id='fig1-employment', config={'displayModeBar': False}), md=6),
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col(dcc.Graph(id='fig1-courses', config={'displayModeBar': False}), md=6),
            dbc.Col(dcc.Graph(id='fig1-tuition', config={'displayModeBar': False}), md=6),
        ]),
        data_sources_footer
    ]),
    className="mt-4 border-0 shadow-lg"
)

tab2_content = dbc.Card(
    dbc.CardBody([
        html.H4("Market Demand", className="card-title text-white mb-4 fw-light"),
        dbc.Row([
            dbc.Col([
                html.Label("Filter by Role:"),
                dcc.Dropdown(
                    id='tab2-role-filter',
                    options=[{'label': r, 'value': r} for r in df_salary['Role'].unique()],
                    value=None,
                    placeholder="Compare All Roles...",
                    clearable=True
                )
            ], width=4)
        ], className="mb-4"),
        dbc.Row([
            dbc.Col(dcc.Graph(id='fig2-openings', config={'displayModeBar': False}), md=6),
            dbc.Col(dcc.Graph(id='fig2-salary', config={'displayModeBar': False}), md=6),
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col(dcc.Graph(id='fig2-skills', config={'displayModeBar': False}), md=6),
            dbc.Col(dcc.Graph(id='fig2-companies', config={'displayModeBar': False}), md=6),
        ]),
        data_sources_footer
    ]),
    className="mt-4 border-0 shadow-lg"
)

tab3_content = dbc.Card(
    dbc.CardBody([
        html.H4("Skill Mismatch (Gap Analysis)", className="card-title text-white mb-4 fw-light"),
        dbc.Row([
            dbc.Col(dcc.Graph(id='fig3-radar', config={'displayModeBar': False}), md=6),
            dbc.Col([
                html.H5("Mismatch Details (Positive = Undersupplied)", className="text-white fw-light mb-3"),
                dash_table.DataTable(
                    id='fig3-table',
                    columns=[{"name": i, "id": i} for i in df_mismatch.columns],
                    data=df_mismatch.to_dict('records'),
                    style_table={'borderRadius': '12px', 'overflow': 'hidden', 'boxShadow': '0 4px 6px rgba(0,0,0,0.5)'},
                    style_header={
                        'backgroundColor': '#27272A',
                        'color': 'white',
                        'fontWeight': 'bold',
                        'border': 'none',
                        'borderBottom': '1px solid #3F3F46'
                    },
                    style_data={
                        'backgroundColor': '#1C1C1E',
                        'color': '#9CA3AF',
                        'border': 'none',
                        'borderBottom': '1px solid rgba(255,255,255,0.05)'
                    },
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
    html.H2("AI & Data Science Talent Supply vs. Market Demand", className="mt-5 mb-4 text-center text-white fw-light"),
    dbc.Tabs([
        dbc.Tab(tab1_content, label="Supply (Educational Pipeline)", tab_id="tab-1"),
        dbc.Tab(tab2_content, label="Demand (Market Requirements)", tab_id="tab-2"),
        dbc.Tab(tab3_content, label="Gap Analysis", tab_id="tab-3"),
    ], id="tabs", active_tab="tab-1", className="nav-pills justify-content-center")
], fluid=True, className="px-5")

# ==========================================
# 4. Callbacks for Tab 1
# ==========================================
@app.callback(
    [Output('fig1-graduates', 'figure'), Output('fig1-employment', 'figure'),
     Output('fig1-courses', 'figure'), Output('fig1-tuition', 'figure')],
    [Input('tab1-program-filter', 'value')]
)
def update_tab1(selected_program):
    d_grad = df_graduates if not selected_program else df_graduates[df_graduates['Program'] == selected_program]
    d_emp = df_employment if not selected_program else df_employment[df_employment['Program'] == selected_program]
    d_course = df_courses if not selected_program else df_courses[df_courses['Program'] == selected_program]
    
    # Neon green line chart
    colors_line = ['#D4FF32', '#34D399', '#60A5FA']
    fig_grad = px.line(d_grad, x='Year', y='Graduates', color='Program', color_discrete_sequence=colors_line, title='Graduates Trend (2021-2024)')
    fig_grad.update_traces(line_shape='spline', mode='lines+markers', marker=dict(size=8, line=dict(width=2, color='DarkSlateGrey')))
    
    # Purple bar chart
    d_emp_melt = d_emp.melt(id_vars=['Program'], value_vars=['Year_1', 'Year_2', 'Year_3'], var_name='Year_After', value_name='Percentage')
    fig_emp = px.bar(d_emp_melt, x='Program', y='Percentage', color='Year_After', barmode='group', color_discrete_sequence=['#8B5CF6', '#A855F7', '#C084FC'], title='Employment Rate (%)')
    fig_emp.update_traces(marker_line_width=0, opacity=0.9)

    d_course_melt = d_course.melt(id_vars=['Program'], value_vars=['Math/Stats', 'Programming', 'Domain/Business'], var_name='Subject', value_name='Weight')
    fig_course = px.bar(d_course_melt, x='Program', y='Weight', color='Subject', barmode='group', color_discrete_sequence=['#3B82F6', '#8B5CF6', '#EC4899'], title='Course Subject Breakdown')
    fig_course.update_traces(marker_line_width=0, opacity=0.9)

    fig_tuit = px.bar(d_grad.groupby('Program')['Tuition_Fee_THB'].mean().reset_index(), 
                      x='Program', y='Tuition_Fee_THB', color_discrete_sequence=['#8B5CF6'], title='Average Tuition Fees (THB)')
    fig_tuit.update_traces(marker_line_width=0, opacity=0.9)
    fig_tuit.update_yaxes(tickformat=",.0f")
                      
    return apply_dark_theme(fig_grad), apply_dark_theme(fig_emp), apply_dark_theme(fig_course), apply_dark_theme(fig_tuit)

# ==========================================
# 5. Callbacks for Tab 2
# ==========================================
@app.callback(
    [Output('fig2-openings', 'figure'), Output('fig2-salary', 'figure'),
     Output('fig2-skills', 'figure'), Output('fig2-companies', 'figure')],
    [Input('tab2-role-filter', 'value')]
)
def update_tab2(selected_role):
    d_open = df_openings if not selected_role else df_openings[df_openings['Role'] == selected_role]
    d_sal = df_salary if not selected_role else df_salary[df_salary['Role'] == selected_role]
    
    colors_line = ['#D4FF32', '#34D399', '#60A5FA']
    fig_open = px.line(d_open, x='Year', y='Openings', color='Role', color_discrete_sequence=colors_line, title='Job Openings Over Time')
    fig_open.update_traces(line_shape='spline', mode='lines+markers', marker=dict(size=8))
    fig_open.update_yaxes(tickformat=",.0f")
    
    salary_levels = ['Entry', 'Mid', 'Senior', 'Executive']
    d_sal_melt = d_sal.melt(id_vars=['Role'], value_vars=salary_levels, var_name='Level', value_name='Salary ($)')
    fig_sal = px.bar(d_sal_melt, x='Role', y='Salary ($)', color='Level', barmode='group', color_discrete_sequence=['#6D28D9', '#8B5CF6', '#A855F7', '#C084FC'], title='Salary by Experience Level')
    fig_sal.update_traces(marker_line_width=0, opacity=0.9)
    fig_sal.update_yaxes(tickformat="$,.0f")
    
    fig_skills = px.bar(df_demand_skills.sort_values('Demand_Count', ascending=True), 
                        x='Demand_Count', y='Skill', orientation='h', color_discrete_sequence=['#8B5CF6'], title='Top Required Skills (% of Job Posts)')
    fig_skills.update_traces(marker_line_width=0, opacity=0.9)
                        
    fig_comp = px.bar(df_companies.sort_values('Open_Roles', ascending=False), 
                      x='Company', y='Open_Roles', color_discrete_sequence=['#10B981'], title='Top Hiring Companies (Sample Vacancies)')
    fig_comp.update_traces(marker_line_width=0, opacity=0.9)
                      
    return apply_dark_theme(fig_open), apply_dark_theme(fig_sal), apply_dark_theme(fig_skills), apply_dark_theme(fig_comp)

# ==========================================
# 6. Callbacks/Figures for Tab 3
# ==========================================
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
            fill='toself',
            name='Supply (Education)',
            line_color='#8B5CF6'
        ))
        fig.add_trace(go.Scatterpolar(
            r=df_mismatch['Demand_Weight'].tolist() + [df_mismatch['Demand_Weight'].tolist()[0]],
            theta=df_mismatch['Skill'].tolist() + [df_mismatch['Skill'].tolist()[0]],
            fill='toself',
            name='Demand (Market)',
            line_color='#D4FF32'
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

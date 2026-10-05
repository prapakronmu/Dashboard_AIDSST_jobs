import dash
from dash import dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# ==========================================
# 1. Mock Data Setup
# ==========================================

# Tab 1 Data
df_graduates = pd.DataFrame({
    'Year': [2021, 2022, 2023, 2024]*3,
    'Program': ['B.S. Data Science']*4 + ['B.S. Statistics']*4 + ['B.E. AI']*4,
    'Graduates': [100, 150, 200, 250, 300, 310, 320, 330, 50, 100, 150, 220],
    'Tuition_Fee_THB': [120000]*4 + [80000]*4 + [150000]*4
})

df_employment = pd.DataFrame({
    'Program': ['B.S. Data Science', 'B.S. Statistics', 'B.E. AI'],
    'Year_1': [70, 60, 85],
    'Year_2': [20, 30, 10],
    'Year_3': [5, 5, 5] # percentages
})

# Dummy data for Tab 1.2
df_courses = pd.DataFrame({
    'Program': ['B.S. Data Science', 'B.S. Statistics', 'B.E. AI'],
    'Math/Stats': [30, 60, 20],
    'Programming': [40, 20, 50],
    'Domain/Business': [30, 20, 30]
})

# Tab 2 Data
df_demand_skills = pd.DataFrame({
    'Skill': ['Python', 'SQL', 'AWS', 'R', 'Machine Learning', 'Deep Learning'],
    'Demand_Count': [800, 600, 450, 300, 750, 400]
})

df_salary = pd.DataFrame({
    'Role': ['Data Scientist', 'Statistician', 'AI Engineer'],
    'Entry': [35000, 25000, 45000],
    'Mid': [60000, 45000, 80000],
    'Senior': [120000, 80000, 150000]
})

# Dummy data for Tab 2.1
df_openings = pd.DataFrame({
    'Year': [2021, 2022, 2023, 2024]*3,
    'Role': ['Data Scientist']*4 + ['Statistician']*4 + ['AI Engineer']*4,
    'Openings': [500, 650, 800, 1000, 300, 320, 310, 350, 200, 400, 750, 1200]
})

# Dummy data for Tab 2.3
df_companies = pd.DataFrame({
    'Company': ['TechCorp', 'DataSys', 'FinBank', 'HealthAI', 'RetailX'],
    'Open_Roles': [120, 85, 95, 60, 40]
})

# Tab 3 Data (Mismatch)
df_mismatch = pd.DataFrame({
    'Skill': ['Python', 'SQL', 'AWS', 'R', 'Machine Learning'],
    'Supply_Weight': [80, 50, 10, 90, 70],
    'Demand_Weight': [95, 80, 70, 30, 85]
})
df_mismatch['Mismatch'] = df_mismatch['Demand_Weight'] - df_mismatch['Supply_Weight']


# ==========================================
# 2. App Initialization
# ==========================================
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
app.title = "AI & DS Talent Dashboard"

# ==========================================
# 3. Layout Definitions
# ==========================================

# Tab 1 Layout (Supply)
tab1_content = dbc.Card(
    dbc.CardBody([
        html.H4("Educational Pipeline (Supply)", className="card-title"),
        dbc.Row([
            dbc.Col([
                html.Label("Filter by Program:"),
                dcc.Dropdown(
                    id='tab1-program-filter',
                    options=[{'label': p, 'value': p} for p in df_graduates['Program'].unique()],
                    value=None,
                    placeholder="All Programs",
                    clearable=True
                )
            ], width=4)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col(dcc.Graph(id='fig1-graduates'), md=6),
            dbc.Col(dcc.Graph(id='fig1-employment'), md=6),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='fig1-courses'), md=6),
            dbc.Col(dcc.Graph(id='fig1-tuition'), md=6),
        ])
    ]),
    className="mt-3"
)

# Tab 2 Layout (Demand)
tab2_content = dbc.Card(
    dbc.CardBody([
        html.H4("Market Demand", className="card-title"),
        dbc.Row([
            dbc.Col([
                html.Label("Filter by Role:"),
                dcc.Dropdown(
                    id='tab2-role-filter',
                    options=[{'label': r, 'value': r} for r in df_salary['Role'].unique()],
                    value=None,
                    placeholder="All Roles",
                    clearable=True
                )
            ], width=4)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col(dcc.Graph(id='fig2-openings'), md=6),
            dbc.Col(dcc.Graph(id='fig2-salary'), md=6),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='fig2-skills'), md=6),
            dbc.Col(dcc.Graph(id='fig2-companies'), md=6),
        ])
    ]),
    className="mt-3"
)

# Tab 3 Layout (Gap Analysis)
tab3_content = dbc.Card(
    dbc.CardBody([
        html.H4("Skill Mismatch (Gap Analysis)", className="card-title"),
        dbc.Row([
            dbc.Col(dcc.Graph(id='fig3-radar'), md=6),
            dbc.Col([
                html.H5("Mismatch Details (Positive = Undersupplied, Negative = Oversupplied)"),
                dash_table.DataTable(
                    id='fig3-table',
                    columns=[{"name": i, "id": i} for i in df_mismatch.columns],
                    data=df_mismatch.to_dict('records'),
                    style_cell={'textAlign': 'left', 'padding': '10px'},
                    style_header={
                        'backgroundColor': 'rgb(230, 230, 230)',
                        'fontWeight': 'bold'
                    },
                    sort_action='native'
                )
            ], md=6),
        ])
    ]),
    className="mt-3"
)

app.layout = dbc.Container([
    html.H2("AI & Data Science Talent Supply vs. Market Demand", className="mt-4 mb-4 text-center"),
    dbc.Tabs([
        dbc.Tab(tab1_content, label="Supply (Educational Pipeline)", tab_id="tab-1"),
        dbc.Tab(tab2_content, label="Demand (Market Requirements)", tab_id="tab-2"),
        dbc.Tab(tab3_content, label="Gap Analysis", tab_id="tab-3"),
    ], id="tabs", active_tab="tab-1")
], fluid=True)

# ==========================================
# 4. Callbacks for Tab 1
# ==========================================
@app.callback(
    [Output('fig1-graduates', 'figure'),
     Output('fig1-employment', 'figure'),
     Output('fig1-courses', 'figure'),
     Output('fig1-tuition', 'figure')],
    [Input('tab1-program-filter', 'value')]
)
def update_tab1(selected_program):
    # Filter logic
    d_grad = df_graduates if not selected_program else df_graduates[df_graduates['Program'] == selected_program]
    d_emp = df_employment if not selected_program else df_employment[df_employment['Program'] == selected_program]
    d_course = df_courses if not selected_program else df_courses[df_courses['Program'] == selected_program]
    
    # 1.1 Graduates by Degree Program
    fig_grad = px.line(d_grad, x='Year', y='Graduates', color='Program', markers=True, title='Graduates by Program (2021-2024)')
    
    # 1.3 Employment Rate
    # Melt the employment data for stacked bar chart
    d_emp_melt = d_emp.melt(id_vars=['Program'], value_vars=['Year_1', 'Year_2', 'Year_3'], var_name='Year_After', value_name='Percentage')
    fig_emp = px.bar(d_emp_melt, x='Program', y='Percentage', color='Year_After', title='Employment Rate Post-Graduation (%)')
    
    # 1.2 Courses Alignment
    d_course_melt = d_course.melt(id_vars=['Program'], value_vars=['Math/Stats', 'Programming', 'Domain/Business'], var_name='Subject', value_name='Weight')
    fig_course = px.bar(d_course_melt, x='Program', y='Weight', color='Subject', barmode='group', title='Course Distribution by Subject Area')
    
    # 1.4 Tuition Fees
    fig_tuit = px.bar(d_grad.groupby('Program')['Tuition_Fee_THB'].mean().reset_index(), 
                      x='Program', y='Tuition_Fee_THB', title='Average Tuition Fees (THB)', color='Program')
                      
    return fig_grad, fig_emp, fig_course, fig_tuit

# ==========================================
# 5. Callbacks for Tab 2
# ==========================================
@app.callback(
    [Output('fig2-openings', 'figure'),
     Output('fig2-salary', 'figure'),
     Output('fig2-skills', 'figure'),
     Output('fig2-companies', 'figure')],
    [Input('tab2-role-filter', 'value')]
)
def update_tab2(selected_role):
    # Filtering
    d_open = df_openings if not selected_role else df_openings[df_openings['Role'] == selected_role]
    d_sal = df_salary if not selected_role else df_salary[df_salary['Role'] == selected_role]
    
    # Note: df_demand_skills and df_companies are static in this mock as they don't map directly to 'Role' in dummy data yet,
    # but could be filtered if we expand the mock data.
    
    # 2.1 Job Openings by Role
    fig_open = px.line(d_open, x='Year', y='Openings', color='Role', markers=True, title='Job Openings by Role over Time')
    
    # 2.4 Salary by Experience Level
    d_sal_melt = d_sal.melt(id_vars=['Role'], value_vars=['Entry', 'Mid', 'Senior'], var_name='Level', value_name='Salary')
    fig_sal = px.bar(d_sal_melt, x='Role', y='Salary', color='Level', barmode='group', title='Salary Ranges by Experience Level')
    
    # 2.2 Top Required Skills
    fig_skills = px.bar(df_demand_skills.sort_values('Demand_Count', ascending=True), 
                        x='Demand_Count', y='Skill', orientation='h', title='Top Required Skills')
                        
    # 2.3 Top Hiring Companies
    fig_comp = px.bar(df_companies.sort_values('Open_Roles', ascending=False), 
                      x='Company', y='Open_Roles', title='Top Hiring Companies')
                      
    return fig_open, fig_sal, fig_skills, fig_comp

# ==========================================
# 6. Callbacks/Figures for Tab 3 (Static for now)
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
            name='Supply (Education)'
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=df_mismatch['Demand_Weight'].tolist() + [df_mismatch['Demand_Weight'].tolist()[0]],
            theta=df_mismatch['Skill'].tolist() + [df_mismatch['Skill'].tolist()[0]],
            fill='toself',
            name='Demand (Market)'
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100])
            ),
            title='Skill Supply vs Demand'
        )
        return fig
    return dash.no_update

if __name__ == '__main__':
    app.run_server(debug=True)

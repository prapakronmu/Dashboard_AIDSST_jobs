# 🚀 Handoff Prompt for Antigravity (Dashboard Generation)

**Instruction for User/AI Agent:**
Read the following Business Requirements Document (BRD) carefully. Your task is to generate a fully functional, interactive web-based dashboard using **Python (Backend)** and **Dash by Plotly (Frontend/Visualizations)**. 

---

## 1. Project Overview
**Project Name:** AI & Data Science Talent Supply vs. Market Demand Dashboard
**Objective:** To build an interactive dashboard answering two main questions: 
1. What is the supply of graduates and their learned skills? 
2. What is the market demand (job openings) and required skills?
3. What is the skill mismatch between supply and demand?

## 2. Technical Stack
*   **Backend framework / UI:** Python with `Dash` (dash-bootstrap-components for layout).
*   **Data Visualization:** `Plotly` (plotly.express / plotly.graph_objects).
*   **Data Manipulation:** `pandas`.

## 3. UI/UX & Interactivity Requirements
*   **Layout:** A modern, clean layout with a top navigation bar or sidebar to switch between **3 Tabs**.
*   **Cross-Filtering (CRITICAL):** Every chart within a specific tab MUST be interconnected using Dash Callbacks. For example, in Tab 1, if a user clicks on a specific Degree Program, all other charts in Tab 1 (Courses, Employment Rate, Tuition) must dynamically filter to show data ONLY for that selected program.
*   **Theme:** Professional corporate theme (e.g., Dash Bootstrap CYBORG or FLATLY theme).

---

## 4. Dashboard Structure & Features

### 🟢 TAB 1: Supply (ปริมาณคนที่จบ และ Skills ที่เรียนมา)
**Objective:** Track the educational pipeline producing AI, Data Science, and Statistics professionals.

*   **Chart 1.1: Graduates by Degree Program (Bar/Line Chart)**
    *   *Data:* Names of degree programs (e.g., B.S. Data Science, B.S. Statistics, B.E. AI) and the number of graduates produced per year.
    *   *Interaction:* Clicking a bar/line filters Charts 1.2, 1.3, and 1.4.
*   **Chart 1.2: Mandatory Courses Alignment (Heatmap or Table)**
    *   *Data:* List of mandatory courses for each program, categorized by 3 tracks: AI, Data Science, and Statistics.
*   **Chart 1.3: Employment Rate Post-Graduation (Stacked Bar Chart)**
    *   *Data:* Number/Percentage of graduates securing jobs in Year 1, Year 2, and Year 3 after graduation.
*   **Chart 1.4: Tuition Fees (KPI Cards or Horizontal Bar Chart)**
    *   *Data:* Average tuition fees for the selected programs.

### 🔵 TAB 2: Demand (ปริมาณงานที่จ้าง และ Skill ที่ต้องการ)
**Objective:** Track market demand, required competencies, and compensation.

*   **Chart 2.1: Job Openings by Role (Time Series / Line Chart)**
    *   *Data:* Number of vacancies for AI Engineer, Data Scientist, Statistician over time.
    *   *Interaction:* Clicking a role filters Charts 2.2, 2.3, and 2.4.
*   **Chart 2.2: Top Required Skills (Horizontal Bar Chart or Treemap)**
    *   *Data:* Most frequently mentioned skills in job postings (e.g., Python, SQL, AWS, LLMs).
*   **Chart 2.3: Top Hiring Companies (Bar Chart or Data Table)**
    *   *Data:* Companies actively hiring for these roles.
*   **Chart 2.4: Salary by Experience Level (Box Plot or Grouped Bar Chart)**
    *   *Data:* Salary ranges categorized by Entry-level, Mid-level, and Senior-level.

### 🔴 TAB 3: Gap Analysis (วิเคราะห์ Skill Mismatch)
**Objective:** Compare the skills taught in universities (Tab 1) against the skills demanded by employers (Tab 2).

*   **Chart 3.1: Skill Supply vs. Demand (Diverging Bar Chart or Radar Chart)**
    *   *Data:* Overlay of "% of programs teaching Skill X" vs. "% of job postings requiring Skill X".
    *   *Insight:* Visually highlight gaps (e.g., Universities teach R extensively, but employers demand Python and Cloud infrastructure).
*   **Chart 3.2: Mismatch Score Details (Interactive Table)**
    *   *Data:* List of skills highlighting "Over-supplied" and "Under-supplied" skills.

---

## 5. Mock Data Setup (Python Dict/Pandas DataFrame)
*AI Agent: Please use the following dummy data structures to ensure the app is fully runnable upon generation.*

```python
# Mock Data for Dash App
import pandas as pd

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

# Tab 3 Data (Mismatch)
df_mismatch = pd.DataFrame({
    'Skill': ['Python', 'SQL', 'AWS', 'R', 'Machine Learning'],
    'Supply_Weight': [80, 50, 10, 90, 70],
    'Demand_Weight': [95, 80, 70, 30, 85]
})
```

## 6. Execution Command
Write a complete, single-file `app.py` script using Dash and Plotly. Include the mock data above. Implement the tabs, layout, and strictly ensure that the Dash `@app.callback` functions are correctly set up to filter the graphs within Tab 1 and Tab 2 based on user clicks or dropdown selections.
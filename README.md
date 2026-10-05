# AI & Data Science Talent Supply vs. Market Demand Dashboard

## Project Overview
This project aims to build an interactive dashboard to visualize the current landscape of the AI, Data Science, and Statistics job market. It addresses three main questions:
1. **Supply**: What is the supply of graduates and their learned skills?
2. **Demand**: What is the market demand (job openings) and required skills?
3. **Gap Analysis**: What is the skill mismatch between supply and demand?

## Technical Stack Options
Based on the initial handoff documents, there are two potential technical stacks for this dashboard:

### Option A: Python / Dash (Preferred for Data Science workflows)
*   **Backend framework / UI:** Python with `Dash` (dash-bootstrap-components for layout).
*   **Data Visualization:** `Plotly` (plotly.express / plotly.graph_objects).
*   **Data Manipulation:** `pandas`.

### Option B: React / Tailwind CSS
*   **Frontend:** React.js, Tailwind CSS for styling (Glassmorphism or crisp SaaS UI).
*   **Charts:** Recharts or Chart.js.

## Dashboard Structure (Dash Approach)
The dashboard is divided into three main tabs:
1. **Supply (Tab 1)**: Tracks the educational pipeline producing AI/DS professionals, including graduates by program, courses, employment rates, and tuition fees.
2. **Demand (Tab 2)**: Tracks market demand, required competencies, job openings by role, top skills, top companies, and salaries.
3. **Gap Analysis (Tab 3)**: Compares the skills taught in universities against those demanded by employers to highlight over-supplied and under-supplied skills.

## Features & Interactivity
- **Cross-Filtering**: Charts within specific tabs are interconnected (e.g., clicking a degree program filters related charts).
- **Responsive Layout**: Professional corporate theme (e.g., CYBORG or FLATLY) with a top navigation bar or sidebar.
- **Hover tooltips** on all charts.

# 🚀 Handoff Prompt for Antigravity (Dashboard Generation)

**Instruction for User:**
Copy the entire text below the line and paste it into Antigravity (or your preferred UI/Code Generation AI) to generate the interactive dashboard.

## System Persona

Act as an expert Frontend Developer and Data Visualization UI/UX Designer. Your task is to build a modern, responsive, and interactive dashboard using React, Tailwind CSS, and a charting library (like Recharts or Chart.js).

## Project: AI & Data Science Job Market Dashboard

**Objective:** Create an interactive dashboard that visualizes the current landscape of the AI, Data Science, and Statistics job market, including salaries, required skills, and hiring trends based on real-world Open Data.

## 🎨 UI & Layout Specifications

The dashboard should have a clean, modern "Glassmorphism" or crisp SaaS-like UI. Use a neutral background (e.g., `bg-gray-50`) with white cards for content.

1. **Top Navigation / Header:**
   * Dashboard Title: "AI & Data Job Market Insights"
   * Global Filters (Mock UI dropdowns): "Select Country", "Select Role (AI/DS/Stats)", "Experience Level".

2. **KPI Cards (Top Row):**
   * **Card 1:** Avg Entry-Level Salary (\$85,000)
   * **Card 2:** Most Demanded Skill (Python)
   * **Card 3:** YoY Job Growth (+24%)
   * **Card 4:** Top Employer Industry (Tech & Finance)

3. **Main Visualizations (Grid Layout):**
   * **Chart 1 (Bar Chart): Top 10 Required Skills** (Python, SQL, R, Machine Learning, AWS, etc.)
   * **Chart 2 (Area/Line Chart): Hiring Demand vs Graduates (2019-2025)** showing the widening gap.
   * **Chart 3 (Box Plot or Grouped Bar Chart): Salary by Experience Level** (EN, MI, SE, EX).

4. **Bottom Section (Data Table):**
   * "Top Employers & Minimum Qualifications" Table (Columns: Company, Open Roles, Required Degree, Location).

5. **Footer / Data Sources Section:**
   * A subtle, clean footer displaying the Open Data sources used for this dashboard, with clickable links.

## 🛠 Features & Interactivity

* Hover tooltips on all charts.
* Responsive grid (1 column on mobile, 2-3 columns on desktop).
* Use standard Lucide-react icons for the KPI cards.

## 📊 Mock Data (JSON Format)

Use this data to populate the charts, tables, and footer so the dashboard is fully functional upon rendering:

```json
{
  "kpis": {
    "entrySalary": "$85k",
    "topSkill": "Python (78%)",
    "growth": "+24.5%",
    "activeJobs": "142,500"
  },
  "skillsData": [
    { "skill": "Python", "demand": 82 },
    { "skill": "SQL", "demand": 75 },
    { "skill": "Machine Learning", "demand": 68 },
    { "skill": "R", "demand": 45 },
    { "skill": "AWS/Cloud", "demand": 50 },
    { "skill": "LLMs/GenAI", "demand": 42 },
    { "skill": "Statistics", "demand": 38 }
  ],
  "salaryByLevel": [
    { "level": "Entry (EN)", "min": 60000, "avg": 85000, "max": 120000 },
    { "level": "Mid (MI)", "min": 90000, "avg": 135000, "max": 180000 },
    { "level": "Senior (SE)", "min": 130000, "avg": 185000, "max": 250000 },
    { "level": "Executive (EX)", "min": 180000, "avg": 240000, "max": 400000 }
  ],
  "hiringVsGraduates": [
    { "year": "2020", "graduates": 45000, "jobs": 50000 },
    { "year": "2021", "graduates": 52000, "jobs": 75000 },
    { "year": "2022", "graduates": 61000, "jobs": 110000 },
    { "year": "2023", "graduates": 75000, "jobs": 145000 },
    { "year": "2024", "graduates": 88000, "jobs": 190000 }
  ],
  "topEmployers": [
    { "company": "Google (Alphabet)", "roles": "AI Engineer, Data Scientist", "degree": "MS/PhD", "location": "Remote / USA" },
    { "company": "Booz Allen Hamilton", "roles": "Data Scientist, Statistician", "degree": "BS/MS", "location": "USA" },
    { "company": "JP Morgan Chase", "roles": "Quantitative Analyst, ML Engineer", "degree": "MS", "location": "Global" },
    { "company": "OpenAI", "roles": "Research Scientist, AI Engineer", "degree": "PhD", "location": "USA" }
  ],
  "dataSources": [
    { "name": "Stanford AI Index Report Dataset", "url": "https://github.com/ai-index-hai-stanford/" },
    { "name": "Data Science, AI & ML Job Salaries (Kaggle)", "url": "https://www.kaggle.com/datasets/adilshamim8/salaries-for-data-science-jobs/data" },
    { "name": "AI & Data Job Market Roles & Skills (Kaggle)", "url": "https://www.kaggle.com/datasets/anujsaha0123456789/ai-and-data-job-market-2023-roles-skills-and" },
    { "name": "U.S. Bureau of Labor Statistics (BLS) - Occupational Employment", "url": "https://www.bls.gov/ooh/math/data-scientists.htm" }
  ]
}
```

## ⚡ Execution Command

Please generate the complete, self-contained frontend code for this dashboard based on the specs and mock data provided above. Make sure it is visually stunning, ready to be presented, and clearly displays the Open Data sources in the footer or a dedicated section.
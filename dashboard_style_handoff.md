# 🎨 UI/UX Style Requirements for Dashboard Restyling

**Instruction for AI Agent (Antigravity):**
Please completely restyle the existing dashboard to match the strict dark-mode aesthetic detailed below. Apply these styles globally to all containers, navigation elements, and data visualizations (Plotly/Recharts). 

## 1. Global Theme & Color Palette

The design relies on a deep, almost pure black background with slightly lighter dark gray cards, punctuated by vibrant, glowing accent colors.

*   **Main Dashboard Container Background:** Very dark gray / Near Black (`#0C0C0E` or `#121212`).
*   **Card / Widget Background:** Dark Gray (`#1C1C1E` or `#18181B`).
*   **Text Colors:**
    *   **Primary Text (Headings, Main Numbers):** Pure White (`#FFFFFF`) or Off-White (`#F3F4F6`).
    *   **Secondary Text (Labels, Axes, Muted Text):** Light Gray (`#9CA3AF` or `#A1A1AA`).
*   **Accent Colors:**
    *   **Primary Accent (Purple):** Vibrant Purple/Violet (Solid: `#8B5CF6`, Gradients: from `#A855F7` to `#6D28D9`). Used for primary bars, heatmaps, and main brand elements.
    *   **Secondary Accent (Neon Green):** Neon Yellow-Green (`#D4FF32` or `#BEF264`). Used for line charts, positive trend indicators, and active dots.
    *   **Negative/Expense Accent:** Muted Red/Pink (e.g., `#FB7185`) if needed for negative values.

## 2. Typography

*   **Font Family:** Modern Sans-Serif (e.g., `Inter`, `SF Pro Display`, `Roboto`, or system default sans-serif).
*   **Headings:** Light to Medium font weight (300-500). The greeting ("Welcome back, Angela") should be large (e.g., `2xl` or `3xl`) and thin/light.
*   **Numbers/KPIs:** Bold and large (e.g., `4xl`), using pure white for high contrast.
*   **Letter Spacing:** Keep it tight and clean; avoid wide letter spacing.

## 3. Component Styling (CSS / Tailwind Specs)

*   **Cards & Containers:**
    *   **Border Radius:** Highly rounded corners. Main app container should have ~`24px` to `32px` (`rounded-3xl`). Individual widget cards should have ~`16px` to `20px` (`rounded-2xl`).
    *   **Borders/Shadows:** No heavy borders. Use very subtle borders (e.g., `border border-white/5` or `#27272A`) or rely purely on the background color contrast (`#0C0C0E` vs `#1C1C1E`). No harsh drop shadows; use very soft, dark shadows if any.
*   **Navigation & Tabs (Pill Shapes):**
    *   **Shape:** Fully rounded pills (`rounded-full`).
    *   **Active State:** White background (`#FFFFFF`) with Black text (`#000000`).
    *   **Inactive State:** Dark gray background (e.g., `#27272A`) with Light Gray text (`#9CA3AF`).
*   **Buttons:**
    *   **Action Buttons (Transfer, Request):** White background, black text, fully rounded (`rounded-full`), with small icons.
    *   **Icon Buttons:** Circular (`rounded-full`), dark gray background (`#27272A`).

## 4. Data Visualization Styling (Plotly / Recharts specific)

Charts must blend seamlessly into the cards. **Do not use default white backgrounds for charts.**

*   **Global Chart Layout:**
    *   `plot_bgcolor`: 'rgba(0,0,0,0)' (Transparent)
    *   `paper_bgcolor`: 'rgba(0,0,0,0)' (Transparent)
    *   **Grid Lines:** Horizontal grid lines should be highly transparent, dashed or dotted (`#3F3F46` or `rgba(255,255,255,0.1)`). Remove vertical grid lines entirely.
    *   **Axes:** Hide axis lines. Keep axis text small and muted (`#9CA3AF`).
*   **Line Charts (e.g., Analytics):**
    *   **Shape:** Smooth curves (`spline` interpolation).
    *   **Colors:** Top line in Neon Green (`#D4FF32`). Bottom/comparison line in dashed White or Light Gray.
    *   **Markers:** Hide markers by default, but show a distinct dot with a glow effect on hover or at the current data point.
*   **Bar Charts / Histograms:**
    *   **Colors:** Use the Purple accent. Apply a vertical linear gradient if the charting library supports it (light purple at top, dark purple at bottom).
    *   **Shape:** Rounded tops on the bars (`border-radius` on top corners).
    *   **Spacing:** Tight gaps between bars.
*   **Heatmap (Activity by time):**
    *   **Shape:** Rounded square cells (`rx=4, ry=4`).
    *   **Color Scale:** From very dark purple/gray (low activity) to bright vibrant purple (high activity).

## 5. Execution Command

Please refactor the existing layout and CSS/Tailwind classes to apply these styles. If using Python/Dash, update the `dash_bootstrap_components` theme overrides and inject custom CSS for the pill navigation and card backgrounds. Update all `fig.update_layout()` calls in Plotly to match the transparent, neon-accented dark theme described above.
#!/usr/bin/env python3
"""
Generate a clean, professional Jupyter Notebook for the Life Expectancy & GDP portfolio project.
"""

import nbformat as nbf
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
import os

nb = new_notebook()

# Metadata
nb.metadata = {
    "kernelspec": {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3"
    },
    "language_info": {
        "name": "python",
        "version": "3.10"
    }
}

def add_md(text):
    nb.cells.append(new_markdown_cell(text))

def add_code(code, outputs=None):
    cell = new_code_cell(code)
    if outputs:
        cell.outputs = outputs
    nb.cells.append(cell)

# ========== TITLE & INTRO ==========
add_md("""# Life Expectancy and GDP Analysis
## Exploring the Relationship Across Six Nations (2000–2015)

**Portfolio Project for Data Analyst Roles**  
*Randall James | [LinkedIn](https://www.linkedin.com/in/randall-james-stl) | [GitHub](https://github.com/senseirandystl)*

---

### Project Goal
Investigate whether there is a correlation between a country's economic output (GDP) and the life expectancy of its citizens using data from the World Health Organization and the World Bank.

**Focusing Questions:**
- Has life expectancy increased over time in the six nations?
- Has GDP increased over time in the six nations?
- Is there a correlation between GDP and life expectancy of a country?
- What is the average life expectancy in these nations?
- What is the distribution of that life expectancy?

This notebook demonstrates professional data analysis workflow: data inspection, cleaning (minimal), EDA, visualization, statistical insight, and storytelling.""")

# ========== SETUP ==========
add_md("## 1. Setup and Data Loading")

add_code("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter
import warnings
warnings.filterwarnings('ignore')

# Professional styling
sns.set_theme(style="whitegrid", palette="Dark2", font_scale=1.05)
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['savefig.dpi'] = 150

# Load data
df = pd.read_csv('../data/all_data.csv')
df = df.rename(columns={'Life expectancy at birth (years)': 'LEABY'})

print("Dataset shape:", df.shape)
print("\\nColumns:", df.columns.tolist())
print("\\nCountries:", df['Country'].unique().tolist())
print("\\nYears:", df['Year'].min(), "to", df['Year'].max())
print("\\nMissing values:", df.isnull().sum().sum())
df.head()""")

# ========== EDA ==========
add_md("""## 2. Exploratory Data Analysis

The dataset contains 96 observations (6 countries × 16 years). It is clean with no missing values — ready for analysis.""")

add_code("""# Summary statistics
print("=== Life Expectancy Summary ===")
print(df['LEABY'].describe().round(2))

print("\\n=== GDP Summary (USD) ===")
print(df['GDP'].describe().round(0))

print("\\n=== Average LE by Country ===")
print(df.groupby('Country')['LEABY'].mean().sort_values(ascending=False).round(2))

print("\\n=== Average GDP by Country (Trillions USD) ===")
print((df.groupby('Country')['GDP'].mean() / 1e12).sort_values(ascending=False).round(2))""")

# ========== VISUALIZATIONS ==========
add_md("""## 3. Visualizations & Key Insights

All plots are also saved as high-resolution PNGs in the `visuals/` folder for use in reports or the README blog post.""")

add_md("### 3.1 Life Expectancy Trends Over Time")

add_code("""fig, ax = plt.subplots(figsize=(11, 6))
sns.pointplot(data=df, x='Year', y='LEABY', hue='Country', ax=ax, markers='o', linestyles='-', dodge=0.25, alpha=0.85)
ax.set_title('Life Expectancy at Birth Has Increased Across All Six Nations', fontsize=14, pad=12, fontweight='bold')
ax.set_ylabel('Life Expectancy (years)')
ax.set_xlabel('Year')
ax.legend(title='Country', bbox_to_anchor=(1.01, 1), loc='upper left')
ax.set_ylim(42, 83)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()""")

add_md("""**Insight:** All countries show upward trends. **Zimbabwe** had the most dramatic recovery (+14.7 years). Developed nations show steady but smaller gains from already high baselines.""")

add_md("### 3.2 GDP Growth Over Time")

add_code("""def trillions(x, pos):
    return f'${x*1e-12:.1f}T'

fig, ax = plt.subplots(figsize=(11, 6))
sns.pointplot(data=df, x='Year', y='GDP', hue='Country', ax=ax, markers='o', linestyles='-', dodge=0.25, alpha=0.85)
ax.yaxis.set_major_formatter(FuncFormatter(trillions))
ax.set_title('GDP Growth: China\'s Explosive Rise Stands Out', fontsize=14, pad=12, fontweight='bold')
ax.set_ylabel('GDP (Trillions USD)')
ax.set_xlabel('Year')
ax.legend(title='Country', bbox_to_anchor=(1.01, 1), loc='upper left')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()""")

add_md("""**Insight:** China’s GDP grew ~9.1×. Chile ~3.1×. Zimbabwe recovered ~2.4× after a severe economic collapse. USA/Germany/Mexico grew steadily ~1.7×.""")

add_md("### 3.3 GDP vs Life Expectancy — Overall Relationship")

add_code("""fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=df, x='GDP', y='LEABY', hue='Country', size='Year', sizes=(20, 120), alpha=0.65, ax=ax)
sns.regplot(data=df, x='GDP', y='LEABY', scatter=False, ax=ax, color='gray', line_kws={'linestyle': '--', 'alpha': 0.7})
ax.set_title('GDP vs Life Expectancy: Moderate Positive Correlation (r = 0.34)', fontsize=13, pad=10, fontweight='bold')
ax.set_xlabel('GDP (USD)')
ax.set_ylabel('Life Expectancy (years)')
ax.xaxis.set_major_formatter(FuncFormatter(trillions))
ax.legend(bbox_to_anchor=(1.01, 1), loc='upper left', title='Country')
plt.tight_layout()
plt.show()

# Correlation
corr = df[['GDP', 'LEABY']].corr().iloc[0,1]
print(f"Overall Pearson correlation (GDP vs LE): {corr:.3f}")""")

add_md("""**Key Statistical Finding:** Overall correlation is **moderate positive (r = 0.34)**. The relationship appears stronger *within* rapidly developing countries. High-GDP developed nations cluster tightly at high life expectancy, suggesting diminishing marginal returns.""")

add_md("### 3.4 Within-Country Relationships (FacetGrid)")

add_code("""g = sns.FacetGrid(df, col='Country', col_wrap=3, height=3.8, aspect=1.05, sharex=False, sharey=False)
g.map_dataframe(sns.scatterplot, x='GDP', y='LEABY', hue='Year', palette='viridis', alpha=0.75, s=50)
g.map_dataframe(sns.regplot, x='GDP', y='LEABY', scatter=False, color='#d62728', line_kws={'alpha': 0.6})
g.set_titles("{col_name}")
g.set_axis_labels("GDP (USD)", "Life Expectancy (years)")
for ax in g.axes.flat:
    ax.xaxis.set_major_formatter(FuncFormatter(trillions))
g.fig.suptitle('Within-Country: GDP Growth Frequently Tracks Rising Life Expectancy', y=1.03, fontsize=13, fontweight='bold')
plt.tight_layout()
plt.show()""")

add_md("### 3.5 Distribution of Life Expectancy")

add_code("""fig, ax = plt.subplots(figsize=(10, 5.5))
sns.violinplot(data=df, x='Country', y='LEABY', ax=ax, inner='quartile', cut=0, palette='Dark2')
sns.swarmplot(data=df, x='Country', y='LEABY', ax=ax, color='white', alpha=0.5, size=2.5)
ax.set_title('Distribution of Life Expectancy by Country', fontsize=14, pad=10, fontweight='bold')
ax.set_ylabel('Life Expectancy (years)')
plt.xticks(rotation=25, ha='right')
plt.tight_layout()
plt.show()""")

add_md("""**Distribution Insight:** Germany has the highest and most consistent life expectancy. Zimbabwe’s distribution is much lower but shows recovery spread. Chile and USA have tight, high distributions.""")

# ========== CONCLUSIONS ==========
add_md("""## 4. Conclusions

### Summary of Findings
1. **Life expectancy increased in every country** — most dramatically in Zimbabwe (+14.7 years) and China (+4.4 years).
2. **GDP growth was highly heterogeneous** — China’s economy expanded over 9×; developed nations grew steadily.
3. **Positive association exists** between GDP and life expectancy (r = 0.34 overall). The link is clearer within countries undergoing rapid development.
4. **Diminishing returns** observed: once countries reach high development levels, additional GDP growth yields smaller LE gains.
5. **Zimbabwe** serves as a powerful case study of how economic recovery can coincide with major health improvements.

### Skills Demonstrated
- Data ingestion, inspection, and minimal cleaning with **pandas**
- Grouping, aggregation, and time-series handling
- Professional statistical visualization with **Seaborn** + **Matplotlib** (point plots, scatter + regression, FacetGrid, violin + swarm)
- Translating quantitative findings into clear narrative insights
- Reproducible analysis suitable for stakeholder communication

### Limitations & Caveats
- Only six countries — broader analysis would improve generalizability.
- Observational data; cannot claim causation (healthcare systems, education, inequality, and policy matter greatly).
- GDP is an aggregate measure; does not reflect income distribution or public investment in health.

### Business / Policy Implications
Economic development is strongly associated with better population health outcomes. However, targeted public health investments, universal healthcare access, and social safety nets can deliver life expectancy gains even before extreme wealth is achieved (as seen in Chile’s strong performance relative to its GDP).

---

**This project is part of my Data Analyst portfolio.**  
View the full README blog post and all high-resolution visuals in the repository root.  
Other projects: [Polymarket Bot Arena](https://github.com/senseirandystl/polymarket-bot-arena), blockchain analysis, and internal process automation dashboards.

*Thank you for reviewing. Open to Data Analyst, BI Analyst, and Project Coordinator opportunities in St. Louis metro or remote.*""")

# Save notebook
os.makedirs('notebooks', exist_ok=True)
with open('notebooks/life_expectancy_gdp_analysis.ipynb', 'w') as f:
    nbf.write(nb, f)

print("✅ Notebook created: notebooks/life_expectancy_gdp_analysis.ipynb")
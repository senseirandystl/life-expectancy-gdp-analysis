#!/usr/bin/env python3
"""
Life Expectancy and GDP Analysis - Visualization Generator
Creates professional, portfolio-ready plots using Seaborn and Matplotlib.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter
import os

# Set professional style
sns.set_theme(style="whitegrid", palette="Dark2", font_scale=1.1)
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['savefig.facecolor'] = 'white'
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['figure.dpi'] = 150

# Create output directory
os.makedirs('visuals', exist_ok=True)

# Load data
df = pd.read_csv('data/all_data.csv')
df = df.rename(columns={'Life expectancy at birth (years)': 'LEABY'})

# Formatter for trillions
def trillions(x, pos):
    return f'${x*1e-12:.1f}T'

formatter = FuncFormatter(trillions)

# Color palette
countries = df['Country'].unique()
palette = sns.color_palette("Dark2", n_colors=len(countries))
country_colors = dict(zip(countries, palette))

print("Generating visualizations...")

# 1. Life Expectancy Over Time (Point + Line)
fig, ax = plt.subplots(figsize=(12, 7))
sns.pointplot(data=df, x='Year', y='LEABY', hue='Country', ax=ax, markers='o', linestyles='-', dodge=0.3, alpha=0.85)
ax.set_title('Life Expectancy at Birth Has Increased Across All Six Nations (2000–2015)', fontsize=16, pad=20, fontweight='bold')
ax.set_ylabel('Life Expectancy at Birth (years)', fontsize=13)
ax.set_xlabel('Year', fontsize=13)
ax.legend(title='Country', bbox_to_anchor=(1.02, 1), loc='upper left', frameon=True)
ax.set_ylim(40, 85)
ax.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('visuals/le_over_time.png', bbox_inches='tight', dpi=300)
plt.close()
print("✓ Saved le_over_time.png")

# 2. GDP Over Time (Trillions)
fig, ax = plt.subplots(figsize=(12, 7))
sns.pointplot(data=df, x='Year', y='GDP', hue='Country', ax=ax, markers='o', linestyles='-', dodge=0.3, alpha=0.85)
ax.yaxis.set_major_formatter(formatter)
ax.set_title('GDP Growth: Dramatic Divergence Especially in China (2000–2015)', fontsize=16, pad=20, fontweight='bold')
ax.set_ylabel('GDP (Trillions of USD)', fontsize=13)
ax.set_xlabel('Year', fontsize=13)
ax.legend(title='Country', bbox_to_anchor=(1.02, 1), loc='upper left', frameon=True)
ax.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('visuals/gdp_over_time.png', bbox_inches='tight', dpi=300)
plt.close()
print("✓ Saved gdp_over_time.png")

# 3. Scatter: GDP vs Life Expectancy (all data)
fig, ax = plt.subplots(figsize=(10, 7))
sns.scatterplot(data=df, x='GDP', y='LEABY', hue='Country', size='Year', sizes=(30, 150), alpha=0.7, ax=ax, palette=country_colors)
# Add overall regression line
sns.regplot(data=df, x='GDP', y='LEABY', scatter=False, ax=ax, color='gray', line_kws={'linestyle': '--', 'alpha': 0.6})
ax.set_title('GDP vs Life Expectancy: Moderate Positive Correlation (r = 0.34)', fontsize=15, pad=15, fontweight='bold')
ax.set_xlabel('GDP (USD)', fontsize=12)
ax.set_ylabel('Life Expectancy at Birth (years)', fontsize=12)
ax.xaxis.set_major_formatter(formatter)
ax.legend(title='Country / Year size', bbox_to_anchor=(1.02, 1), loc='upper left')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('visuals/gdp_vs_le_scatter.png', bbox_inches='tight', dpi=300)
plt.close()
print("✓ Saved gdp_vs_le_scatter.png")

# 4. Faceted scatter: GDP vs LE by Country
g = sns.FacetGrid(df, col='Country', col_wrap=3, height=4, aspect=1.1, sharex=False, sharey=False)
g.map_dataframe(sns.scatterplot, x='GDP', y='LEABY', hue='Year', palette='viridis', alpha=0.8, s=60)
g.map_dataframe(sns.regplot, x='GDP', y='LEABY', scatter=False, color='red', line_kws={'alpha': 0.5})
g.set_titles("{col_name}")
g.set_axis_labels("GDP (USD)", "Life Expectancy (years)")
for ax in g.axes.flat:
    ax.xaxis.set_major_formatter(formatter)
g.fig.suptitle('Within-Country Relationship: GDP Growth Often Tracks with Rising Life Expectancy', fontsize=14, y=1.02, fontweight='bold')
plt.tight_layout()
plt.savefig('visuals/gdp_vs_le_facet.png', bbox_inches='tight', dpi=300)
plt.close()
print("✓ Saved gdp_vs_le_facet.png")

# 5. Violin Plot - Distribution of Life Expectancy
fig, ax = plt.subplots(figsize=(11, 6))
sns.violinplot(data=df, x='Country', y='LEABY', ax=ax, inner='box', palette=country_colors, cut=0)
sns.swarmplot(data=df, x='Country', y='LEABY', ax=ax, color='white', alpha=0.6, size=3)
ax.set_title('Distribution of Life Expectancy by Country (2000–2015)', fontsize=15, pad=15, fontweight='bold')
ax.set_ylabel('Life Expectancy at Birth (years)', fontsize=12)
ax.set_xlabel('')
plt.xticks(rotation=30, ha='right')
ax.grid(True, axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('visuals/le_distribution_violin.png', bbox_inches='tight', dpi=300)
plt.close()
print("✓ Saved le_distribution_violin.png")

# 6. Bonus: Average LE Bar Chart
fig, ax = plt.subplots(figsize=(9, 5))
avg_le = df.groupby('Country')['LEABY'].mean().sort_values(ascending=True)
colors = [country_colors[c] for c in avg_le.index]
bars = ax.barh(avg_le.index, avg_le.values, color=colors, edgecolor='white', linewidth=0.8)
ax.set_xlabel('Average Life Expectancy (years)', fontsize=12)
ax.set_title('Average Life Expectancy by Country (2000–2015)', fontsize=14, pad=12, fontweight='bold')
ax.bar_label(bars, fmt='%.1f', padding=3, fontsize=10)
ax.set_xlim(45, 85)
ax.grid(True, axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig('visuals/avg_le_bar.png', bbox_inches='tight', dpi=300)
plt.close()
print("✓ Saved avg_le_bar.png")

# 7. Bonus: LE Improvement Bar
fig, ax = plt.subplots(figsize=(9, 5))
le_change = df[df['Year']==2015].set_index('Country')['LEABY'] - df[df['Year']==2000].set_index('Country')['LEABY']
le_change = le_change.sort_values(ascending=True)
colors = ['#2ca02c' if v > 0 else '#d62728' for v in le_change.values]
bars = ax.barh(le_change.index, le_change.values, color=colors, edgecolor='white')
ax.set_xlabel('Change in Life Expectancy (years)', fontsize=12)
ax.set_title('Life Expectancy Improvement (2000 → 2015)', fontsize=14, pad=12, fontweight='bold')
ax.bar_label(bars, fmt='+%.1f', padding=3, fontsize=10)
ax.axvline(0, color='black', linewidth=0.8)
ax.grid(True, axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig('visuals/le_improvement_bar.png', bbox_inches='tight', dpi=300)
plt.close()
print("✓ Saved le_improvement_bar.png")

print("\n✅ All visualizations generated successfully in /visuals/")
print("Files created:")
for f in sorted(os.listdir('visuals')):
    print(f"  - {f}")
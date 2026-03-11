import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load Data
df = pd.read_csv('email.csv', nrows=10000)
df['date'] = pd.to_datetime(df['date'])
df['hour'] = df['date'].dt.hour

# 2. Professional Styling
sns.set_theme(style="whitegrid")
plt.figure(figsize=(12, 7))

# 3. Create Annotated Plot
ax = sns.countplot(data=df, x='hour', hue='hour', palette='viridis', legend=False)

# Add clear titles for judges
plt.title('Email Activity Baseline: Establishing "Normal" Behavior', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Hour of Day (00:00 - 23:00)', fontsize=12)
plt.ylabel('Email Volume', fontsize=12)

# 4. Add Contextual Annotations (The "Sell")
plt.annotate('Normal Peak Business Hours', xy=(8, 1750), xytext=(11, 1800),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1))

plt.annotate('High-Risk "After-Hours" Zone', xy=(21, 50), xytext=(16, 400),
             arrowprops=dict(facecolor='red', shrink=0.05, width=1),
             color='red', fontweight='bold')

plt.tight_layout()
plt.savefig('Barclays_Baseline_Final.png', dpi=300)
plt.show()
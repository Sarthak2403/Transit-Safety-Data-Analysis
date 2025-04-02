import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
from matplotlib.gridspec import GridSpec

# Connection to database
conn = sqlite3.connect('transit_safety.db')

plt.figure(figsize=(18, 20))
gs = GridSpec(3, 2, figure=plt.gcf())

# 1. Accident Trend
ax1 = plt.subplot(gs[0, 0])
trend_df = pd.read_sql("""
    SELECT Year, COUNT(*) as accidents 
    FROM transit_safety 
    GROUP BY Year ORDER BY Year
""", conn)
ax1.plot(trend_df['Year'], trend_df['accidents'], marker='o')
ax1.set_title('Accident Trend Over Time')
ax1.set_xlabel('Year')
ax1.set_ylabel('Accidents')
ax1.grid(True)

# 2. Injury Severity
ax2 = plt.subplot(gs[0, 1])
severity_df = pd.read_sql("""
    SELECT 
        SUM("Total Injuries") as injuries,
        SUM("Total Serious Injuries") as serious_injuries
    FROM transit_safety
""", conn)
severity_df.T.plot(kind='bar', ax=ax2, legend=False)
ax2.set_title('Injury Severity Breakdown')
ax2.set_ylabel('Count')

# 3. Mode Comparison
ax3 = plt.subplot(gs[1, 0])
mode_df = pd.read_sql("""
    SELECT "Mode Name", COUNT(*) as accidents 
    FROM transit_safety 
    GROUP BY "Mode Name"
""", conn)
mode_df.plot(kind='bar', x='Mode Name', y='accidents', ax=ax3, legend=False)
ax3.set_title('Accidents by Transportation Mode')
ax3.set_ylabel('Accidents')

# 4. Training Completion (example - needs your training data)
ax4 = plt.subplot(gs[1, 1])
ax4.set_title('Safety Training Completion')
ax4.text(0.5, 0.5, 'Training data visualization\n(connect to your training database)', 
         ha='center', va='center')
ax4.set_ylabel('Completion Rate (%)')

# 5. Near Miss Reports
ax5 = plt.subplot(gs[2, 0])
ax5.set_title('Near Miss Reports Trend')
ax5.text(0.5, 0.5, 'Near-miss data visualization\n(connect to your reporting system)', 
         ha='center', va='center')

# 6. Safety Audit Findings (example)
ax6 = plt.subplot(gs[2, 1])
ax6.set_title('Safety Audit Findings')
ax6.text(0.5, 0.5, 'Audit data visualization\n(connect to your audit database)', 
         ha='center', va='center')

# Final formatting
plt.tight_layout()
plt.suptitle('Transit Safety Dashboard', y=1.02, fontsize=16)
plt.show()
conn.close()
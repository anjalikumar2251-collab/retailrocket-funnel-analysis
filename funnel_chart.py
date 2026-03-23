import sqlite3
import matplotlib.pyplot as plt

conn = sqlite3.connect('retailrocket.db')
cursor = conn.cursor()

# Query 1 - Funnel stages
q1 = """SELECT event, COUNT(DISTINCT visitorid) as total
FROM events GROUP BY event"""
funnel_data = cursor.execute(q1).fetchall()

# Query 2 - Busiest hours
q2 = """SELECT STRFTIME('%H', DATETIME(timestamp/1000, 'unixepoch')) as hour,
COUNT(*) as total FROM events
GROUP BY hour ORDER BY total DESC LIMIT 10"""
hours_data = cursor.execute(q2).fetchall()

# Query 3 - Top 10 items
q3 = """SELECT itemid, COUNT(*) as total_views
FROM events WHERE event = 'view'
GROUP BY itemid ORDER BY total_views DESC LIMIT 10"""
items_data = cursor.execute(q3).fetchall()

conn.close()

# Prepare data
stages = ['View', 'Add to Cart', 'Purchase']
values = [1404179, 37722, 11719]

hours = [row[0] for row in hours_data]
hour_counts = [row[1] for row in hours_data]

items = [str(row[0]) for row in items_data]
item_views = [row[1] for row in items_data]

# Create 3 charts in one figure
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.suptitle('Retailrocket E-Commerce Funnel Analysis', fontsize=16, fontweight='bold')

# Chart 1 - Funnel
axes[0].bar(stages, values, color=['#2196F3', '#FF9800', '#4CAF50'])
axes[0].set_title('Funnel Stages')
axes[0].set_ylabel('Unique Visitors')
for i, v in enumerate(values):
    axes[0].text(i, v + 10000, f'{v:,}', ha='center', fontsize=9)

# Chart 2 - Busiest hours
axes[1].bar(hours, hour_counts, color='#9C27B0')
axes[1].set_title('Busiest Hours of Day')
axes[1].set_xlabel('Hour (24hr)')
axes[1].set_ylabel('Total Events')

# Chart 3 - Top 10 items
axes[2].barh(items[::-1], item_views[::-1], color='#F44336')
axes[2].set_title('Top 10 Most Viewed Items')
axes[2].set_xlabel('Total Views')

plt.tight_layout()
plt.savefig('funnel_analysis_complete.png', dpi=150)
plt.show()
print("Chart saved as funnel_analysis_complete.png")
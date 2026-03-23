import pandas as pd
import sqlite3

print("Loading CSV...")
df = pd.read_csv(r"C:\Users\Anjali S\Desktop\Kaggle RetailRocket\events.csv")

print("Creating database...")
conn = sqlite3.connect('retailrocket.db')

print("Writing to database...")
df.to_sql('events', conn, if_exists='replace', index=False)

conn.close()
print("Done! Database created: retailrocket.db")
print(f"Total rows loaded: {len(df):,}")

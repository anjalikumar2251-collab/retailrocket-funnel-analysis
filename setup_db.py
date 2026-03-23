import os
import pandas as pd
import sqlite3

print("Loading CSV...")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(BASE_DIR, "events.csv"))

print("Creating database...")
conn = sqlite3.connect(os.path.join(BASE_DIR, 'retailrocket.db'))

print("Writing to database...")
df.to_sql('events', conn, if_exists='replace', index=False)

conn.close()
print("Done! Database created: retailrocket.db")
print(f"Total rows loaded: {len(df):,}")

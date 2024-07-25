import os
import pandas as pd
import sqlite3

# Load the DataFrame
data = pd.read_csv('final.csv')

def create_database():
    conn = sqlite3.connect('./furniture.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS furniture (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Category TEXT,
            Name TEXT,
            Image_Path TEXT,
            Description TEXT,
            Style TEXT
        )
    ''')
    conn.commit()
    conn.close()

create_database()

def populate_database(dataframe):
    conn = sqlite3.connect('./furniture.db')
    c = conn.cursor()
    
    # Convert DataFrame to list of tuples
    furniture_items = dataframe[['Category', 'Style', 'Name', 'Image_Path', 'Description']].values.tolist()
    
    # Insert data into the database
    c.executemany('INSERT INTO furniture (Category, Style, Name, Image_Path, Description) VALUES (?, ?, ?, ?, ?)', furniture_items)
    conn.commit()
    conn.close()

populate_database(data)

def fetch_recommendations(detected_items, name):
    conn = sqlite3.connect('./furniture.db')
    c = conn.cursor()
    recommendations = []
    
    for item in detected_items:
        c.execute('SELECT * FROM furniture WHERE category=? AND name=?', (item, name))
        recommendations.extend(c.fetchall())  # Using extend to handle multiple recommendations
    
    conn.close()
    return recommendations

# Example usage
recommendations = fetch_recommendations(['Bar-furniture'], 'Bar-stool')
for rec in recommendations:
    print(rec)

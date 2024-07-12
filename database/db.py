import sqlite3

def create_database():
    conn = sqlite3.connect('furniture.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS furniture (
            id INTEGER PRIMARY KEY,
            style TEXT,
            type TEXT,
            image_path TEXT,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

create_database()

def populate_database():
    conn = sqlite3.connect('furniture.db')
    c = conn.cursor()
    furniture_items = [
        ('modern', 'bed', 'path/to/bed.jpg', 'Modern bed description'),
        ('modern', 'chair', 'path/to/chair.jpg', 'Modern chair description'),
        ('modern', 'lamp', 'path/to/lamp.jpg', 'Modern lamp description')]
    c.executemany('INSERT INTO furniture (style, type, image_path, description) VALUES (?, ?, ?, ?)', furniture_items)
    conn.commit()
    conn.close()

populate_database()

def fetch_recomendations(detected_items, style):
    conn = sqlite3.connect('furniture.db')
    c = conn.cursor()
    recomendations = []
    for item in detected_items:
        c.execute('SELECT * FROM furniture WHERE type=? AND style=?', (item, style))
        recomendations.append(c.fetchone())

    conn.close()
    return recomendations

print(fetch_recomendations(['chair'], 'modern'))
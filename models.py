import sqlite3
import os

# Use /app/data/games.db in Docker, games.db locally
DATABASE_DIR = os.environ.get('DATABASE_DIR', '.')
DATABASE_PATH = os.path.join(DATABASE_DIR, 'games.db')

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    # Ensure the database directory exists
    os.makedirs(os.path.dirname(DATABASE_PATH) if os.path.dirname(DATABASE_PATH) else '.', exist_ok=True)
    
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            steam_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            developer TEXT,
            publisher TEXT,
            positive_reviews INTEGER,
            negative_reviews INTEGER,
            owners TEXT,
            average_playtime INTEGER,
            median_playtime INTEGER,
            price TEXT,
            languages TEXT,
            genre TEXT,
            image_url TEXT,
            added_date TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_game_to_db(game_data):
    conn = get_db_connection()
    try:
        conn.execute('''
            INSERT INTO games (
                steam_id, name, developer, publisher, positive_reviews,
                negative_reviews, owners, average_playtime, median_playtime,
                price, languages, genre, image_url, added_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            game_data['steam_id'], game_data['name'], game_data['developer'],
            game_data['publisher'], game_data['positive_reviews'],
            game_data['negative_reviews'], game_data['owners'],
            game_data['average_playtime'], game_data['median_playtime'],
            game_data['price'], game_data['languages'], game_data['genre'],
            game_data['image_url'], game_data['added_date']
        ))
        conn.commit()
    except sqlite3.IntegrityError:
        # Game already exists
        pass
    finally:
        conn.close()

def get_all_games():
    conn = get_db_connection()
    games = conn.execute('SELECT * FROM games ORDER BY added_date DESC').fetchall()
    conn.close()
    return games

def get_game_by_id(game_id):
    conn = get_db_connection()
    game = conn.execute('SELECT * FROM games WHERE id = ?', (game_id,)).fetchone()
    conn.close()
    return game

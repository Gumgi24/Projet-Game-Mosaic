from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, Response
from flask import session as flask_session
import os
import sqlite3
import requests
from functools import wraps
import json
from datetime import datetime
import hashlib
from dotenv import load_dotenv
import signal
import sys

# Load environment variables
load_dotenv()

# Import our custom modules
from models import init_db, add_game_to_db, get_all_games, get_game_by_id
from auth import check_auth, hash_password

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# Initialize database
init_db()

# Basic Auth decorator
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

# Routes
@app.route('/')
@requires_auth
def index():
    games = get_all_games()
    return render_template('index.html', games=games)

@app.route('/add_game', methods=['GET', 'POST'])
@requires_auth
def add_game():
    if request.method == 'POST':
        steam_id = request.form.get('steam_id')
        
        if not steam_id:
            flash('Please enter a Steam ID', 'error')
            return redirect(url_for('add_game'))
        
        # Fetch game data from SteamSpy API
        try:
            # Get data from SteamSpy
            steamspy_url = f"https://steamspy.com/api.php?request=appdetails&appid={steam_id}"
            steamspy_response = requests.get(steamspy_url, timeout=10)
            steamspy_data = steamspy_response.json()
            
            if 'name' not in steamspy_data or not steamspy_data['name']:
                flash('Invalid Steam ID or game not found', 'error')
                return redirect(url_for('add_game'))
            
            # Get image from Steam Store API
            steamstore_url = f"https://store.steampowered.com/api/appdetails?appids={steam_id}"
            steamstore_response = requests.get(steamstore_url, timeout=10)
            steamstore_data = steamstore_response.json()
            
            # Extract image URL
            image_url = ""
            if str(steam_id) in steamstore_data and steamstore_data[str(steam_id)]['success']:
                image_url = steamstore_data[str(steam_id)]['data'].get('header_image', '')
            
            # Prepare game data for storage
            game_data = {
                'steam_id': steam_id,
                'name': steamspy_data.get('name', ''),
                'developer': steamspy_data.get('developer', ''),
                'publisher': steamspy_data.get('publisher', ''),
                'positive_reviews': steamspy_data.get('positive', 0),
                'negative_reviews': steamspy_data.get('negative', 0),
                'owners': steamspy_data.get('owners', ''),
                'average_playtime': steamspy_data.get('average_forever', 0),
                'median_playtime': steamspy_data.get('median_forever', 0),
                'price': steamspy_data.get('price', ''),
                'languages': steamspy_data.get('languages', ''),
                'genre': steamspy_data.get('genre', ''),
                'image_url': image_url,
                'added_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Add to database
            add_game_to_db(game_data)
            flash(f"Game '{game_data['name']}' added successfully!", 'success')
            return redirect(url_for('index'))
            
        except Exception as e:
            flash(f'Error fetching game data: {str(e)}', 'error')
            return redirect(url_for('add_game'))
    
    return render_template('add_game.html')

@app.route('/game/<int:game_id>')
@requires_auth
def game_detail(game_id):
    game = get_game_by_id(game_id)
    if not game:
        flash('Game not found', 'error')
        return redirect(url_for('index'))
    return render_template('game_detail.html', game=game)

@app.route('/api/game/<int:game_id>')
@requires_auth
def api_game_detail(game_id):
    game = get_game_by_id(game_id)
    if not game:
        return jsonify({'error': 'Game not found'}), 404
    
    # Convert game data to dictionary
    game_dict = {
        'id': game[0],
        'steam_id': game[1],
        'name': game[2],
        'developer': game[3],
        'publisher': game[4],
        'positive_reviews': game[5],
        'negative_reviews': game[6],
        'owners': game[7],
        'average_playtime': game[8],
        'median_playtime': game[9],
        'price': game[10],
        'languages': game[11],
        'genre': game[12],
        'image_url': game[13],
        'added_date': game[14]
    }
    return jsonify(game_dict)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

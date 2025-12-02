# Game Backlog Manager

A web application for managing a shared backlog of games to play with your partner. Built with Python Flask and Tailwind CSS, this app allows you to add games by their Steam ID and view them as beautiful vertical capsules.

## Quick Deployment with Docker

The easiest way to deploy this application is using Docker. Follow these steps:

1. Install Docker:
   - For macOS: Download [Docker Desktop for Mac](https://docs.docker.com/desktop/install/mac-install/)
   - For Windows: Download [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/)
   - For Linux: Follow the [Docker Engine installation guide](https://docs.docker.com/engine/install/)

2. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Projet-Game-Mosaic
   ```

3. Build and run with Docker Compose:
   ```bash
   docker-compose up -d
   ```

4. Access the application at `http://localhost:5001`

5. Log in with the default credentials:
   - Username: `admin`
   - Password: `password`

6. To stop the application:
   ```bash
   docker-compose down
   ```

For production deployment, you can either:
1. Update the environment variables directly in `docker-compose.yml` with your own secure credentials, or
2. Create a `.env` file (copy from `.env.example`) and use `docker-compose.prod.yml` which reads from environment variables.

## Features

- **Game Dashboard**: View all games in your backlog as vertical capsules (similar to Steam library view)
- **Add Games**: Add games using their Steam ID
- **Game Details**: View detailed information about each game including:
  - Review scores and statistics
  - Player counts and playtime data
  - Pricing information
  - Developer and publisher details
  - Supported languages
- **Basic Authentication**: Secure access with username/password authentication
- **Responsive Design**: Works on desktop and mobile devices

## Technologies Used

- **Backend**: Python Flask
- **Frontend**: Tailwind CSS with Font Awesome icons
- **Database**: SQLite
- **APIs**: 
  - SteamSpy API for game metadata
  - Steam Store API for game images

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Projet-Game-Mosaic
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   - Copy `.env.example` to `.env`: `cp .env.example .env`
   - Edit the `.env` file to set your preferred username and password
   - To change the password, generate a new SHA256 hash:
     ```bash
     python -c "import hashlib; print(hashlib.sha256(('your-password' + 'your-salt').encode()).hexdigest())"
     ```

## Usage

1. Start the application:
   ```bash
   python app.py
   ```

2. Open your browser and navigate to `http://localhost:5000`

3. Log in with the credentials set in your `.env` file (default: admin/password)

4. Add games to your backlog by entering their Steam ID:
   - Find the Steam ID in the game's store URL (e.g., for `https://store.steampowered.com/app/730/`, the ID is `730`)

## Project Structure

```
Projet-Game-Mosaic/
├── app.py                 # Main Flask application
├── models.py              # Database models and functions
├── auth.py                # Authentication functions
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
├── games.db               # SQLite database (created automatically)
├── static/                # Static files (CSS, JS, images)
└── templates/             # HTML templates
    ├── base.html          # Base template
    ├── index.html         # Dashboard with game capsules
    ├── add_game.html      # Form to add games by Steam ID
    └── game_detail.html   # Detailed game view
```

## API Sources

This application uses two APIs to gather game information:

1. **SteamSpy API** (`https://steamspy.com/api.php`) - Provides game metadata, review statistics, and player data
2. **Steam Store API** (`https://store.steampowered.com/api/appdetails`) - Provides game images and additional details

## Security Notes

- Default credentials are `admin` / `password` - please change these in production
- The application uses Basic HTTP Authentication
- Passwords are hashed using SHA256 with a salt
- All data is stored locally in an SQLite database

## Customization

You can customize the appearance by modifying the Tailwind CSS configuration in `templates/base.html`.

## License

This project is open source and available under the MIT License.

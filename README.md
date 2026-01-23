Movie Manager Bot
A Telegram bot for managing a personal movie collection. The bot allows users to add, search, filter, edit, and delete movies, as well as view detailed information about each entry. The project is built using Python and the Aiogram 3 framework.

Features
Core Functionality
- Display the full list of movies
- Add new movies to the database
- Search movies by title
- Search movies by actor
- Filter movies by genre
- Edit movie information
- Delete movies
- View detailed movie information including description, rating, genre, actors, and poster
Additional Capabilities
- Support for posters provided as:
- Telegram photo
- Image file
- URL link
- Inline keyboard navigation
- Structured callback data
- Logging of function calls

Technologies Used
- Python 3.10+
- Aiogram 3
- Pydantic
- JSON for data storage
- Requests for downloading images

Project Structure
project/
│
├── bot.py                # Main bot logic
├── commands.py           # Command definitions and filters
├── functions.py          # JSON file operations
├── keyboards.py          # Inline keyboard builders
├── models.py             # Pydantic Movie model
├── data.json             # Movie database
├── config.py             # Bot token configuration
├── data.py               # Additional data utilities
├── external.py           # External helper functions
├── file.jpg              # Temporary image file used for poster downloads
├── log.txt               # Log file for function call tracking
└── README.md             # Documentation


Installation and Setup
1. Clone the repository
git clone <repository-url>
cd project


2. Install dependencies
pip install -r requirements.txt


3. Configure the bot token
Create or edit the file config.py:
BOT_TOKEN = "8560338551:AAHmPtimrZLNlbqSVF6UfgDI9vUo5R-tkRA"


4. Run the bot
python bot.py



Data Format (movies.json)
Each movie entry follows this structure:
{
  "name": "Interstellar",
  "description": "Interstellar is a 2014 epic science fiction film...",
  "rating": 8.6,
  "genre": "Science Fiction",
  "actors": ["Matthew McConaughey", "Anne Hathaway"],
  "poster": "https://example.com/poster.jpg"
}



Available Commands
|  |  | 
| /start |  | 
| /movies |  | 
| /create_movie |  | 
| /search_movie |  | 
| /search_by_actor |  | 
| /filter_movies |  | 
| /delete_movie |  | 
| /edit_movie |  | 



Notes
- The bot uses a JSON file as a simple database.
- All operations are asynchronous.
- The project is structured for clarity and maintainability.

License
This project is free to use and modify.

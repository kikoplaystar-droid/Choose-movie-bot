# commands.py — module that defines all bot commands and their filters
from aiogram.filters import Command
from aiogram.types.bot_command import BotCommand

# -------------------- Command Filters --------------------
MOVIE_COMMAND = Command("movies")
START_COMMAND = Command("start")
MOVIE_CREATE_COMMAND = Command("create_movie")
MOVIE_SEARCH_COMMAND = Command("search_movie")
MOVIE_FILTER_COMMAND = Command("filter_movies")
MOVIE_DELETE_COMMAND = Command("delete_movie")
MOVIE_SEARCH_BY_ACTOR = Command("search_by_actor")
MOVIE_EDIT_COMMAND = Command("edit_movie")

# -------------------- Bot Command Descriptions --------------------
MOVIES_BOT_COMMAND = BotCommand(
    command="movies",
    description="View the list of movies"
)

START_BOT_COMMAND = BotCommand(
    command="start",
    description="Start the conversation"
)

# -------------------- Full Command List --------------------
BOT_COMMANDS = [
    BotCommand(command="movies", description="View the list of movies"),
    BotCommand(command="start", description="Start the conversation"),
    BotCommand(command="create_movie", description="Add a new movie"),
    BotCommand(command="search_movie", description="Find a movie"),
    BotCommand(command="filter_movies", description="Filter movies"),
    BotCommand(command="delete_movie", description="Delete a movie"),
    BotCommand(command="search_by_actor",
               description="Search a movie by actor"),
    BotCommand(command="edit_movie", description="Edit a movie"),
]

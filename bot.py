# -------------------- Imports --------------------
import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import BOT_TOKEN as TOKEN
from commands import *

from data import *
from keyboards import *
from models import Movie
from functions import *
from external import async_log_function_call


# -------------------- FSM States --------------------
class MovieForm(StatesGroup):
    name = State()
    description = State()
    rating = State()
    genre = State()
    actors = State()
    poster = State()


class MovieStates(StatesGroup):
    search_query = State()
    filter_criteria = State()
    delete_query = State()
    edit_query = State()
    edit_description = State()
    search_actor = State()


# -------------------- Dispatcher --------------------
dp = Dispatcher()


# -------------------- /start Command --------------------
@dp.message(Command("start"))
async def start(message: Message) -> None:
    await message.answer(
        f"Hello, {message.from_user.full_name}!\n"
        "I am the first bot created by a Python developer Koval Kyrylo Oleksandrovich."
    )


# -------------------- Show All Movies --------------------
@dp.message(MOVIE_COMMAND)
async def movies(message: Message) -> None:
    username = message.from_user.username
    data = get_movies(username)
    markup = movies_keyboard_markup(movies_list=data)
    await message.answer(
        "List of movies. Tap on a movie title to see more details.",
        reply_markup=markup
    )


# -------------------- Helper: Send Movie Info --------------------
async def send_info(movie: Movie, message: Message):
    text = (
        f"Movie: {movie.name}\n"
        f"Description: {movie.description}\n"
        f"Rating: {movie.rating}\n"
        f"Genre: {movie.genre}\n"
        f"Actors: {', '.join(movie.actors)}\n"
    )

    poster = movie.poster

    if poster.startswith("http://") or poster.startswith("https://"):
        await message.answer_photo(
            caption=text,
            photo=FSInputFile(
                save_image(poster),
                filename=f"{movie.name}_poster.{poster.split('.')[-1]}"
            )
        )
    else:
        await message.answer_photo(
            caption=text,
            photo=poster,
        )


# -------------------- Callback: Movie Details --------------------
@dp.callback_query(MovieCallback.filter())
async def callb_movie(callback: CallbackQuery, callback_data: MovieCallback) -> None:
    username = callback.from_user.username
    movie_id = callback_data.id
    movie_data = get_movies(username, movie_id=movie_id)

    if not movie_data:
        await callback.message.answer("Movie not found.")
        return

    movie = Movie(**movie_data)
    await send_info(movie, callback.message)


# -------------------- Movie Search --------------------
@dp.message(MOVIE_SEARCH_COMMAND)
async def search_movie(message: Message, state: FSMContext):
    await message.reply("Enter movie's name to find:")
    await state.set_state(MovieStates.search_query)


@dp.message(MovieStates.search_query)
async def get_search_query(message: Message, state: FSMContext):
    username = message.from_user.username
    query = message.text.lower()
    movies_list = get_movies(username)
    results = [movie for movie in movies_list if query in movie['name'].lower()]

    if results:
        for movie in results:
            await send_info(Movie(**movie), message)
    else:
        await message.reply("Movie not found.")

    await state.clear()


# -------------------- Movie Search By Actor --------------------
@dp.message(MOVIE_SEARCH_BY_ACTOR)
async def search_movie_by_actor(message: Message, state: FSMContext):
    await message.reply("Enter the actor's name to find movies:")
    await state.set_state(MovieStates.search_actor)


@dp.message(MovieStates.search_actor)
async def get_search_query_actor(message: Message, state: FSMContext):
    query = message.text.lower()
    username = message.from_user.username
    movies_list = get_movies(username)

    results = [
        movie for movie in movies_list
        if any(query in actor.lower() for actor in movie['actors'])
    ]

    if results:
        for movie in results:
            await send_info(Movie(**movie), message)
    else:
        await message.reply("No movies found with this actor.")

    await state.clear()


# -------------------- Movies Filter --------------------
@dp.message(MOVIE_FILTER_COMMAND)
async def filter_movies(message: Message, state: FSMContext):
    await message.reply("Enter genre to filter:")
    await state.set_state(MovieStates.filter_criteria)


@dp.message(MovieStates.filter_criteria)
async def get_filter_criteria(message: Message, state: FSMContext):
    movies_list = get_movies()
    criteria = message.text.lower()
    movies_list = sorted(movies_list, key=lambda movie: movie['rating'])
    filtered = list(
        filter(
            lambda movie: criteria in movie['genre'].lower() == criteria,
            movies_list,
        )
    )

    if filtered:
        for movie in filtered:
            await send_info(Movie(**movie), message)
    else:
        await message.reply("No movies found matching these criteria.")

    await state.clear()


# -------------------- Delete Movie --------------------
@dp.message(MOVIE_DELETE_COMMAND)
async def delete_movie_command(message: Message, state: FSMContext):
    await message.reply("Enter the name of the movie you want to delete:")
    await state.set_state(MovieStates.delete_query)


@dp.message(MovieStates.delete_query)
async def get_delete_query(message: Message, state: FSMContext):
    movies_list = get_movies()

    movie_to_delete = message.text.lower()
    for movie in movies_list:
        if movie_to_delete == movie['name'].lower():
            delete_movie(movie)
            await message.reply(f"Movie '{movie['name']}' has been deleted.")
            await state.clear()
            return

    await message.reply("Movie not found.")
    await state.clear()


# -------------------- Movie Edit --------------------
@dp.message(MOVIE_EDIT_COMMAND)
async def edit_movie_command(message: Message, state: FSMContext):
    await message.reply("Enter movie's name, which you want to edit")
    await state.set_state(MovieStates.edit_query)


@dp.message(MovieStates.edit_query)
async def get_edit_query(message: Message, state: FSMContext):
    movie_to_edit = message.text.lower()
    movies = get_movies()
    for movie in movies:
        if movie_to_edit == movie['name'].lower():
            await state.update_data(movie=movie)
            await message.reply("Enter new movie's description: ")
            await state.set_state(MovieStates.edit_description)
            return
    await message.reply("Movie not found.")
    await state.clear()


@dp.message(MovieStates.edit_description)
async def update_description(message: Message, state: FSMContext):
    data = await state.get_data()
    movie = data['movie']
    movie['description'] = message.text
    edit_movie(movie)
    await message.reply(f"Movie '{movie['name']}' updated.")
    await state.clear()

# -------------------- Movie Creation (FSM) --------------------


@dp.message(MOVIE_CREATE_COMMAND)
async def movie_create(message: Message, state: FSMContext) -> None:
    await state.set_state(MovieForm.name)
    await message.answer("Enter the movie title.", reply_markup=None)


@dp.message(MovieForm.name)
async def movie_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(MovieForm.description)
    await message.answer("Enter the movie description.", reply_markup=None)


@dp.message(MovieForm.description)
async def movie_description(message: Message, state: FSMContext) -> None:
    await state.update_data(description=message.text)
    await state.set_state(MovieForm.rating)
    await message.answer("Enter the movie rating (0–10).", reply_markup=None)


@dp.message(MovieForm.rating)
async def movie_rating(message: Message, state: FSMContext) -> None:
    await state.update_data(rating=float(message.text))
    await state.set_state(MovieForm.genre)
    await message.answer("Enter the movie genre.", reply_markup=None)


@dp.message(MovieForm.genre)
async def movie_genre(message: Message, state: FSMContext) -> None:
    await state.update_data(genre=message.text)
    await state.set_state(MovieForm.actors)
    await message.answer(
        "Enter the movie actors separated by ', ' (comma + space).",
        reply_markup=None,
    )


@dp.message(MovieForm.actors)
async def movie_actors(message: Message, state: FSMContext) -> None:
    await state.update_data(actors=[x for x in message.text.split(", ")])
    await state.set_state(MovieForm.poster)
    await message.answer("Send the movie poster (photo, image file, or URL).", reply_markup=None)


@dp.message(MovieForm.poster)
async def movie_poster(message: Message, state: FSMContext) -> None:
    poster_value = None

    if message.photo:
        poster_value = message.photo[-1].file_id
    elif message.document and message.document.mime_type.startswith("image/"):
        poster_value = message.document.file_id
    elif message.text:
        poster_value = message.text

    await state.update_data(poster=poster_value)
    data = await state.get_data()

    movie = Movie(**data)
    add_movie(movie.model_dump())

    await state.clear()
    await message.answer(f"The movie '{movie.name}' has been successfully added!", reply_markup=None)


# -------------------- Echo Handler --------------------
@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")


# -------------------- Bot Startup --------------------
async def main() -> None:
    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    await bot.set_my_commands(BOT_COMMANDS)
    await dp.start_polling(bot)


# -------------------- Entry Point --------------------
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename="log.txt")
    asyncio.run(main())

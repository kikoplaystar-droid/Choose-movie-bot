from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class MovieCallback(CallbackData, prefix="movie", sep=";"):
    id: int
    name: str


def movies_keyboard_markup(
    movies_list: list[dict],
    offset: int | None = None,
    skip: int | None = None
):
    """
    Creates an inline keyboard based on the provided list of movies.

    Example:
    >>> await message.answer(
            text="Some text",
            reply_markup=movies_keyboard_markup(movies_list)
        )
    """

    builder = InlineKeyboardBuilder()
    builder.adjust(1, repeat=True)

    for index, movie_data in enumerate(movies_list):
        callback_data = MovieCallback(id=index, **movie_data)
        builder.button(
            text=callback_data.name,
            callback_data=callback_data.pack()
        )

    builder.adjust(1, repeat=True)
    return builder.as_markup()

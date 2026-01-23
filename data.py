import json


# -------------------- Get All Movies --------------------
def get_all_movies(
    file_path: str = "data.json",
    movie_id: int | None = None
) -> list[dict] | dict:
    """Returns a list of movies or a single movie from file_path."""
    with open(file_path, 'r') as fp:
        movies = json.load(fp)
        if movie_id is not None and movie_id < len(movies):
            return movies[movie_id]
        return movies


# -------------------- Get Movies By Username --------------------
def get_movies(
    username: str,
    file_path: str = "data.json",
    movie_id: int | None = None
) -> list[dict] | dict:
    """Returns a user's movie list or a single movie from file_path."""
    with open(file_path, 'r') as fp:
        movies = json.load(fp)

        if username not in movies.keys():
            return []

        if movie_id is not None and movie_id < len(movies[username]):
            return movies[username][movie_id]

        return movies[username]


# -------------------- Add Movie --------------------
def add_movie(
    movie: dict,
    file_path: str = "movies.json",
):
    """Adds a movie to file_path."""
    movies = get_all_movies(file_path=file_path, movie_id=None)

    if movies is not None:
        movies.append(movie)
        with open(file_path, "w") as fp:
            json.dump(
                movies,
                fp,
                indent=4,
                ensure_ascii=False,
            )


# -------------------- Delete Movie --------------------
def delete_movie(
    movie_to_delete: dict,
    file_path: str = "movies.json",
) -> None:
    """Deletes a movie from file_path by name."""
    movies = get_all_movies(file_path=file_path, movie_id=None)

    movies = [movie for movie in movies if movie["name"]
              != movie_to_delete["name"]]

    with open(file_path, "w") as fp:
        json.dump(
            movies,
            fp,
            indent=4,
            ensure_ascii=False,
        )


# -------------------- Edit Movie --------------------
def edit_movie(
    movie_to_edit: dict,
    file_path: str = "movies.json",
) -> None:
    """Updates a movie description in file_path by name."""
    movies = get_all_movies(file_path=file_path, movie_id=None)

    for i, movie in enumerate(movies):
        if movie_to_edit["name"] == movie["name"]:
            movies[i] = movie_to_edit

    with open(file_path, "w") as fp:
        json.dump(
            movies,
            fp,
            indent=4,
            ensure_ascii=False,
        )

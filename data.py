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
    username: str | None = None,
    file_path: str = "data.json",
    movie_id: int | None = None
):
    with open(file_path, 'r') as fp:
        movies = json.load(fp)

        if username is None:
            return movies

        if username not in movies:
            return []

        if movie_id is not None and movie_id < len(movies[username]):
            return movies[username][movie_id]

        return movies[username]



# -------------------- Add Movie --------------------
def add_movie(
    username: str,
    movie: dict,
    file_path: str = "data.json",
):
    """Adds a movie to file_path."""
    movies = get_all_movies(file_path=file_path, movie_id=None)

    if movies is not None:
        if username not in movies.keys():
            movies[username] = []

        movies[username].append(movie)
        with open(file_path, "w") as fp:
            json.dump(
                movies,
                fp,
                indent=4,
                ensure_ascii=False,
            )


# -------------------- Delete Movie --------------------
def delete_movie(
    username: str,
    movie_to_delete: dict,
    file_path: str = "data.json",
) -> None:
    """Deletes a movie from file_path by name."""
    movies = get_all_movies(file_path=file_path, movie_id=None)

    user_movies = [movie for movie in movies[username] if movie["name"]
              != movie_to_delete["name"]]
    movies[username] = user_movies

    with open(file_path, "w") as fp:
        json.dump(
            movies,
            fp,
            indent=4,
            ensure_ascii=False,
        )
    return True


# -------------------- Edit Movie --------------------
def edit_movie(
        username: str,
    movie_to_edit: dict,
    file_path: str = "data.json",
) -> None:
    """Updates a movie description in file_path by name."""
    movies = get_all_movies(file_path=file_path, movie_id=None)

    for i, movie in enumerate(movies[username]):
        if movie_to_edit["name"] == movie["name"]:
            movies[username][i] = movie_to_edit

    with open(file_path, "w") as fp:
        json.dump(
            movies,
            fp,
            indent=4,
            ensure_ascii=False,
        )

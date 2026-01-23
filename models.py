from pydantic import BaseModel


class Movie(BaseModel):
    """Represents a movie entry stored in the database."""
    name: str
    description: str
    rating: float
    genre: str
    actors: list[str]
    poster: str

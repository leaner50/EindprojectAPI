from pydantic import BaseModel

class Movie(BaseModel):
    title: str
    year: int
    language: str
    directorID: int

    class Config:
        orm_mode = True


class MovieCreate(Movie):
    title: str
    year: int
    language: str
    directorID: int

class MovieDelete(Movie):
    movieID: int

    class Config:
        orm_mode = True

class Director(BaseModel):
    firstName: str
    lastName: str
    gender: str
    
    class Config:
        orm_mode = True


class DirectorCreate(Director):
    firstName: str
    lastName: str
    gender: str

class DirectorUpdate(Director):
    firstName: str
    lastName: str
    gender: str

    class Config:
        orm_mode = True

class Genre(BaseModel):
    genre: str

    class Config:
        orm_mode = True


class GenreCreate(Genre):
    genre: str


class GenreUpdate(Genre):
    genre: str

    class Config:
        orm_mode = True


# class MovieGenre(BaseModel):
#     genreID: int
#     movieID: int

#     class Config:
#         orm_mode = True


# class MovieGenreCreate(MovieGenre):
#     genreID: int
#     movieID: int


# class MovieGenreUpdate(MovieGenre):
#     genreID: int
#     movieID: int

#     class Config:
#         orm_mode = True

class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True
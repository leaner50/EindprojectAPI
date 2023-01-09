from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

import auth
import models
import schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_movie(db: Session, movie_id: int):
    return db.query(models.Movie).filter(models.Movie.movieID == movie_id).first()


def get_movie_by_title(db: Session, title: str):
    return db.query(models.Movie).filter(models.Movie.title == title).first()


def get_movies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Movie).offset(skip).limit(limit).all()


def create_movie(db: Session, movie: schemas.MovieCreate):
    db_movie = models.Movie(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

def delete_movie(db: Session, movie_id: int):
    db_movie = db.query(models.Movie).filter(models.Movie.movieID == movie_id).first()
    db.delete(db_movie)
    db.commit()
    return db_movie

def update_movie(db: Session, movie_id: int, movie: schemas.MovieCreate):
    db_movie = db.query(models.Movie).filter(models.Movie.movieID == movie_id).first()
    if db_movie is None:
        return None
    db_movie.title = movie.title
    db_movie.year = movie.year
    db_movie.language = movie.language
    db_movie.directorID = movie.directorID
    db.commit()
    db.refresh(db_movie)
    return db_movie

def create_director(db: Session, director: schemas.DirectorCreate):
    db_director = models.Director(**director.dict())
    db.add(db_director)
    db.commit()
    db.refresh(db_director)
    return db_director

def create_genre(db: Session, genre: schemas.GenreCreate):
    db_genre = models.Genre(**genre.dict())
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre

# def create_movie_genre(db: Session, movie_genre: schemas.MovieGenreCreate):
#     db_movie_genre = models.MovieGenre(**movie_genre.dict())
#     db.add(db_movie_genre)
#     db.commit()
#     db.refresh(db_movie_genre)
#     return db_movie_genre

def get_director(db: Session, director_id: int):
    return db.query(models.Director).filter(models.Director.directorID == director_id).first()

def get_director_by_name(db: Session, firstName: str, lastName: str):
    return db.query(models.Director).filter(models.Director.firstName == firstName).filter(models.Director.lastName == lastName).first()

def get_directors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Director).offset(skip).limit(limit).all()

def delete_director(db: Session, director_id: int):
    db_director = db.query(models.Director).filter(models.Director.directorID == director_id).first()
    db.delete(db_director)
    db.commit()
    return db_director

def update_director(db: Session, director_id: int, director: schemas.DirectorCreate):
    db_director = db.query(models.Director).filter(models.Director.directorID == director_id).first()
    if db_director is None:
        return None
    db_director.firstName = director.firstName
    db_director.lastName = director.lastName
    db_director.gender = director.gender
    db.commit()
    db.refresh(db_director)
    return db_director

def get_genre(db: Session, genre_id: int):
    return db.query(models.Genre).filter(models.Genre.genreID == genre_id).first()

def get_genre_by_name(db: Session, genre: str):
    return db.query(models.Genre).filter(models.Genre.genre == genre).first()

def get_genres(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Genre).offset(skip).limit(limit).all()

def delete_genre(db: Session, genre_id: int):
    db_genre = db.query(models.Genre).filter(models.Genre.genreID == genre_id).first()
    db.delete(db_genre)
    db.commit()
    return db_genre

def update_genre(db: Session, genre_id: int, genre: schemas.GenreCreate):
    db_genre = db.query(models.Genre).filter(models.Genre.genreID == genre_id).first()
    if db_genre is None:
        return None
    db_genre.genre = genre.genre
    db.commit()
    db.refresh(db_genre)
    return db_genre

# def get_movie_genre(db: Session, movie_id: int, genre_id: int):
#     return db.query(models.MovieGenre).filter(models.MovieGenre.movieID == movie_id).filter(models.MovieGenre.genreID == genre_id).first()

# def get_movie_genres(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.MovieGenre).offset(skip).limit(limit).all()

# def get_movie_genre_by_movie(db: Session, movie_id: int):
#     return db.query(models.MovieGenre).filter(models.MovieGenre.movieID == movie_id).all()

# def delete_movie_genre(db: Session, movie_id: int, genre_id: int):
#     db_movie_genre = db.query(models.MovieGenre).filter(models.MovieGenre.movieID == movie_id).filter(models.MovieGenre.genreID == genre_id).first()
#     db.delete(db_movie_genre)
#     db.commit()
#     return db_movie_genre

# def update_movie_genre(db: Session, movie_id: int, genre_id: int, movie_genre: schemas.MovieGenreCreate):
#     db_movie_genre = db.query(models.MovieGenre).filter(models.MovieGenre.movieID == movie_id).filter(models.MovieGenre.genreID == genre_id).first()
#     if db_movie_genre is None:
#         return None
#     db_movie_genre.movieID = movie_genre.movieID
#     db_movie_genre.genreID = movie_genre.genreID
#     db.commit()
#     db.refresh(db_movie_genre)
#     return db_movie_genre

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

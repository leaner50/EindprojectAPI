from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base

# define the Director model
class Director(Base):
    __tablename__ = 'Director'
    directorID = Column(Integer, primary_key=True)
    firstName = Column(String)
    lastName = Column(String)
    gender = Column(String)

#define the Movie model
class Movie(Base):
    __tablename__ = 'Movie'
    movieID = Column(Integer, primary_key=True)
    title = Column(String)
    year = Column(Integer)
    language = Column(String)
    directorID = Column(Integer, ForeignKey('Director.directorID'))

# define the Genre model
class Genre(Base):
    __tablename__ = 'Genre'
    genreID = Column(Integer, primary_key=True)
    genre = Column(String)

# define the MovieGenre model
class MovieGenre(Base):
    __tablename__ = 'MovieGenre'
    movieGenreID = Column(Integer, primary_key=True)
    genreID = Column(Integer, ForeignKey('Genre.genreID'))
    movieID = Column(Integer, ForeignKey('Movie.movieID'))

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")
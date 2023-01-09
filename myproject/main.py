from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

import os
import crud
import models
import schemas
import auth
from database import SessionLocal, engine

print("We are in the main.......")
if not os.path.exists('.\sqlitedb'):
    print("Making folder.......")
    os.makedirs('.\sqlitedb')

print("Creating tables.......")
models.Base.metadata.create_all(bind=engine)
print("Tables created.......")

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# @app.on_event("startup")
# async def startup_event():
#     print("We are in the startup event.......")
#     db = SessionLocal()
#     print("We are in the startup event.......")
#     num_movies = db.query(models.Movie).count()
#     print("We are in the startup event.......")
#     if num_movies == 0:
#         print("We are in the startup event.......")
#         print("No movies in database, adding some.......")
#         films = [
#             {
#                 "title": "The Shawshank Redemption",
#                 "year": 1994,
#                 "language": "English",
#                 "directorID": 1,
#             }
#         ]
#         for film in films:
#             crud.create_movie(db, schemas.MovieCreate(**film))
#         print("Movies added.......")
#     else:
#         print("Movies already in database.......")
#     print("We are in the startup event.......")
#     num_directors = db.query(models.Director).count()
#     print("We are in the startup event.......")
#     if num_directors == 0:
#         directors = [
#             {
#                 "firstName": "Frank",
#                 "lastName": "Darabont",
#                 "gender": "M",
#             }
#         ]
#         for director in directors:
#             print ("NUMBER",director)
#             crud.create_director(db, schemas.DirectorCreate(**director))
#         print("Directors added.......")
#     else:
#         print("Directors already in database.......")
    
#     num_genres = db.query(models.Genre).count()
#     if num_genres == 0:
#         genres = [
#             {
#                 "genre": "Action",
#             }
#         ]
#         for genre in genres:
#             crud.create_genre(db, schemas.GenreCreate(**genre))
#         print("Genres added.......")
#     else:
#         print("Genres already in database.......")
#     num_movie_genres = db.query(models.MovieGenre).count()
#     if num_movie_genres == 0:
#         movie_genres = [
#             {
#                 "movieID": 1,
#                 "genreID": 1,
#             }
#         ]
#         for movie_genre in movie_genres:
#             crud.create_movie_genre(db, schemas.MovieGenreCreate(**movie_genre))
#         print("Movie genres added.......")
#     else:
#         print("Movie genres already in database.......")
#     db.commit()
#     db.close()

@app.get("/")
def read_root(token: str = Depends(oauth2_scheme)):
    return {"Error": "This is not the page you are looking for"}

@app.get("/movies/", response_model=list[schemas.Movie])
def read_movies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    movies = crud.get_movies(db, skip=skip, limit=limit)
    return movies

@app.get("/movies/{movie_id}", response_model=schemas.Movie)
def read_movie(movie_id: int, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    db_movie = crud.get_movie(db, movie_id=movie_id)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return db_movie

@app.get("/movies/title/{title}", response_model=schemas.Movie)
def read_movie_by_title(title: str, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    db_movie = crud.get_movie_by_title(db, title=title)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return db_movie

@app.post("/movies/", response_model=schemas.Movie)
def create_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    db_movie = crud.get_movie_by_title(db, title=movie.title)
    if db_movie:
        raise HTTPException(status_code=400, detail="Movie already registered")
    return crud.create_movie(db=db, movie=movie)

@app.delete("/movies/{movie_id}", response_model=schemas.Movie)
def delete_movie(movie_id: int, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    db_movie = crud.get_movie(db, movie_id=movie_id)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return crud.delete_movie(db=db, movie_id=movie_id)

@app.put("/movies/{movie_id}")
def update_movie(movie_id: int, movie: schemas.MovieCreate, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    return crud.update_movie(db, movie_id, movie)

@app.get("/directors/", response_model=list[schemas.Director])
def read_directors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    directors = crud.get_directors(db, skip=skip, limit=limit)
    return directors

@app.get("/directors/{director_id}", response_model=schemas.Director)
def read_director(director_id: int, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    db_director = crud.get_director(db, director_id=director_id)
    if db_director is None:
        raise HTTPException(status_code=404, detail="Director not found")
    return db_director

@app.get("/directors/name/{firstName}/{lastName}", response_model=schemas.Director)
def read_director_by_name(firstName: str, lastName: str, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    db_director = crud.get_director_by_name(db, firstName=firstName, lastName=lastName)
    if db_director is None:
        raise HTTPException(status_code=404, detail="Director not found")
    return db_director

@app.post("/directors/", response_model=schemas.Director)
def create_director(director: schemas.DirectorCreate, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    db_director = crud.get_director_by_name(db, firstName=director.firstName, lastName=director.lastName)
    if db_director:
        raise HTTPException(status_code=400, detail="Director already registered")
    return crud.create_director(db=db, director=director)

@app.delete("/directors/{director_id}", response_model=schemas.Director)
def delete_director(director_id: int, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    db_director = crud.get_director(db, director_id=director_id)
    if db_director is None:
        raise HTTPException(status_code=404, detail="Director not found")
    return crud.delete_director(db=db, director_id=director_id)

@app.put("/directors/{director_id}")
def update_director(director_id: int, director: schemas.DirectorCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return crud.update_director(db, director_id, director)

@app.get("/genres/", response_model=list[schemas.Genre])
def read_genres(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    genres = crud.get_genres(db, skip=skip, limit=limit)
    return genres

@app.get("/genres/{genre_id}", response_model=schemas.Genre)
def read_genre(genre_id: int, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    db_genre = crud.get_genre(db, genre_id=genre_id)
    if db_genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    return db_genre

@app.get("/genres/name/{genre}", response_model=schemas.Genre)
def read_genre_by_name(genre: str, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    db_genre = crud.get_genre_by_name(db, genre=genre)
    if db_genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    return db_genre

@app.post("/genres/", response_model=schemas.Genre)
def create_genre(genre: schemas.GenreCreate, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    db_genre = crud.get_genre_by_name(db, genre=genre.genre)
    if db_genre:
        raise HTTPException(status_code=400, detail="Genre already registered")
    return crud.create_genre(db=db, genre=genre)

@app.delete("/genres/{genre_id}", response_model=schemas.Genre)
def delete_genre(genre_id: int, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    db_genre = crud.get_genre(db, genre_id=genre_id)
    if db_genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    return crud.delete_genre(db=db, genre_id=genre_id)

@app.put("/genres/{genre_id}")
def update_genre(genre_id: int, genre: schemas.GenreCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return crud.update_genre(db, genre_id, genre)

# @app.get("/moviegenres/", response_model=list[schemas.MovieGenre])
# def read_moviegenres(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
#     moviegenres = crud.get_movie_genres(db, skip=skip, limit=limit)
#     return moviegenres

# @app.get("/moviegenres/movie/{movie_id}", response_model=list[schemas.MovieGenre])
# def read_moviegenre_by_movie(movie_id: int, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
#     db_moviegenre = crud.get_movie_genre_by_movie(db, movie_id=movie_id)
#     if db_moviegenre is None:
#         raise HTTPException(status_code=404, detail="MovieGenre not found")
#     return db_moviegenre

@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(
        data={"sub": user.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/me", response_model=schemas.User)
def read_users_me(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    current_user = auth.get_current_active_user(db, token)
    return current_user


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items
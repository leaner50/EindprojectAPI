import pytest
import requests
# Change this to the correct base URL for your API
BASE_URL = "http://localhost:8000"
GET_PROTECTED_ENDPOINTS = ["movies", "movies/1", "movies/title/Test Movie", "directors", "directors/1", "directors/name/John/Doe", "genres", "genres/1", "genres/name/Action", "users", "users/me", "items"]
POST_PROTECTED_ENDPOINTS = ["movies", "directors", "genres"]
PUT_PROTECTED_ENDPOINTS = ["movies/1", "directors/1", "genres/1"]
DELETE_PROTECTED_ENDPOINTS = ["movies/1", "directors/1", "genres/1"]

def test_all_get_protected_endpoint():
    for endpoint in GET_PROTECTED_ENDPOINTS:
            response = requests.get(f"{BASE_URL}/{endpoint}")
            assert response.status_code == 401

def test_all_put_protected_endpoint():
    for endpoint in PUT_PROTECTED_ENDPOINTS:
            response = requests.put(f"{BASE_URL}/{endpoint}")
            assert response.status_code == 401

def test_all_post_protected_endpoint():
    for endpoint in POST_PROTECTED_ENDPOINTS:
            response = requests.post(f"{BASE_URL}/{endpoint}")
            assert response.status_code == 401

def test_all_delete_protected_endpoint():
    for endpoint in DELETE_PROTECTED_ENDPOINTS:
            response = requests.delete(f"{BASE_URL}/{endpoint}")
            assert response.status_code == 401

def make_a_user():
    user_data = {
  "email": "string",
  "password": "string"
}
    response = requests.post(f"{BASE_URL}/users", json=user_data)
    assert response.status_code == 200
    
response = requests.post(f"{BASE_URL}/token", data={"username": "string", "password": "string"})
access_token = response.json()["access_token"]
print (access_token)

def test_post_movies():
    movie_data = {
        "title": "Test Movie",
        "year": 2021,
        "language": "English",
        "directorID": 1
    }
    response = requests.post(f"{BASE_URL}/movies", json=movie_data, headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert response.json()["title"] == movie_data["title"]
    assert response.json()["year"] == movie_data["year"]
    assert response.json()["language"] == movie_data["language"]
    assert response.json()["directorID"] == movie_data["directorID"]

def test_put_movies():
    movie_data = {
        "title": "Test Movie",
        "year": 2022,
        "language": "English",
        "directorID": 1
    }
    response = requests.put(f"{BASE_URL}/movies/1", json=movie_data, headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert response.json()["title"] == movie_data["title"]
    assert response.json()["year"] == movie_data["year"]
    assert response.json()["language"] == movie_data["language"]
    assert response.json()["directorID"] == movie_data["directorID"]

def test_get_movies():
    response = requests.get(f"{BASE_URL}/movies", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200

def test_get_movies_by_id():
    response = requests.get(f"{BASE_URL}/movies/1", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert "title" in response.json()
    assert "year" in response.json()
    assert "language" in response.json()
    assert "directorID" in response.json()

def test_get_movies_by_title():
    response = requests.get(f"{BASE_URL}/movies/title/Test Movie", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert "title" in response.json()
    assert "year" in response.json()
    assert "language" in response.json()
    assert "directorID" in response.json()

def test_delete_movies():
    response = requests.delete(f"{BASE_URL}/movies/1", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert "title" in response.json()
    assert "year" in response.json()
    assert "language" in response.json()
    assert "directorID" in response.json()

def test_post_directors():
    director_data = {
        "firstName": "TestFirstName",
        "lastName": "TestLastName",
        "gender": "Female"
    }
    response = requests.post(f"{BASE_URL}/directors", json=director_data, headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert response.json()["firstName"] == director_data["firstName"]
    assert response.json()["lastName"] == director_data["lastName"]
    assert response.json()["gender"] == director_data["gender"]

def test_put_directors():
    director_data = {
        "firstName": "TestFirstName",
        "lastName": "TestLastName",
        "gender": "Male"
    }
    response = requests.put(f"{BASE_URL}/directors/1", json=director_data, headers={"Authorization": f"Bearer {access_token}"})
    assert response.json()["firstName"] == director_data["firstName"]
    assert response.json()["lastName"] == director_data["lastName"]
    assert response.json()["gender"] == director_data["gender"]

def test_get_directors():
    response = requests.get(f"{BASE_URL}/directors", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert "firstName" in response.json()
    assert "gender" in response.json()
    assert "lastName" in response.json()
    

def test_get_directors_by_id():
    response = requests.get(f"{BASE_URL}/directors/1", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert "firstName" in response.json()
    assert "lastName" in response.json()
    assert "gender" in response.json()

def test_get_directors_by_name():
    response = requests.get(f"{BASE_URL}/directors/name/TestFirstName/TestLastName", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert "firstName" in response.json()
    assert "lastName" in response.json()
    assert "gender" in response.json()

def test_delete_directors():
    response = requests.delete(f"{BASE_URL}/directors/1", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert "firstName" in response.json()
    assert "lastName" in response.json()
    assert "gender" in response.json()

def test_post_genres():
    genre_data = {
        "genre": "Test Genre"
    }
    response = requests.post(f"{BASE_URL}/genres", json=genre_data, headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert "genre" in response.json()

def test_put_genres():
    genre_data = {
        "genre": "Test Genre"
    }
    response = requests.put(f"{BASE_URL}/genres/1", json=genre_data, headers={"Authorization": f"Bearer {access_token}"})
    assert "genre" in response.json()

def test_get_genres():
    response = requests.get(f"{BASE_URL}/genres", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert "genre" in response.json()

def test_get_genres_by_id():
    response = requests.get(f"{BASE_URL}/genres/1", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert "genre" in response.json()

def test_get_genres_by_name():
    response = requests.get(f"{BASE_URL}/genres/name/Test Genre", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert "genre" in response.json()

def test_delete_genres():
    response = requests.delete(f"{BASE_URL}/genres/1", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert "genre" in response.json()

def test_get_users():
    response = requests.get(f"{BASE_URL}/users", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200

def test_post_users():
    user_data = {
        "email": "TestUsername",
        "password": "TestPassword"
    }
    response = requests.post(f"{BASE_URL}/users", json=user_data, headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200

def test_get_users_me():
    response = requests.get(f"{BASE_URL}/users/me", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200


def test_get_users_by_id():
    response = requests.get(f"{BASE_URL}/users/1", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200


def test_post_users_items():
    item_data = {
  "title": "string",
  "description": "string"
}
    response = requests.post(f"{BASE_URL}/users/1/items", json=item_data, headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert "id" in response.json()
    assert "owner_id" in response.json()

def test_get_items():
    response = requests.get(f"{BASE_URL}/items", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200

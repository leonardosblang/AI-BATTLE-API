import requests
import pytest

# Test for the root ("/") endpoint
def test_root_endpoint():
    response = requests.get('http://localhost:8000/')
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

# Test for the "/models" endpoint
def test_models_endpoint():
    response = requests.get('http://localhost:8000/models')
    assert response.status_code == 200
    # Perform more assertions depending on the expected structure of your models

# Test for the "/gen-image/{prompt}/{steps}" endpoint
def test_gen_image_endpoint():
    prompt = "test_prompt"
    steps = 5
    response = requests.get(f'http://localhost:8000/gen-image/{prompt}/{steps}')
    assert response.status_code == 200
    # Perform more assertions depending on the expected structure of your response


def test_gen_map_endpoint():
    steps = 5
    response = requests.get(f'http://localhost:8000/gen-rpg/map/{steps}')
    assert response.status_code == 200
    # Perform more assertions depending on the expected structure of your response


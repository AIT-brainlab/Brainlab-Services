from fastapi.testclient import TestClient
from main import app, UserInput,wp_rehash
from mongo_service import MongoService
test_client = TestClient(app)

def test_register()->None:
    resp = test_client.post('/auth/api/register',json={
        'firstname':'raknatee',
        'lastname':'chokluechai',
        'username':'raknatee',
        'email':'raknatee@raknatee.dev',
        'password':'1234'
    })

def test_login()->None:
    resp = test_client.get('/auth/api/login',json={
        'username':'raknatee',
        'password':'1234'
    })

def test_remove_user()->None:
    MongoService.get_user_collection_instance().find_one_and_delete({
        'username':'raknatee'
    })


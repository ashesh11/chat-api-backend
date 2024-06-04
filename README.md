# chat-api-backend

## Pre-requisites
- Python version: 30.10.12

- Redis running at localhost server at port 6379
    - e.g. docker run --name redis-container -p 6379:6379 -d redis

- Install required packages and libraries
    - pip install -r requiments.txt

- .env file is also added in repo. If required, please change the variables.


## Running
- Default sqlite database is used here. Migrate all the migration files.
    - python manage.py migrate

- Start django server
    - python manage.py runserver


## User signup
- url: http://localhost:8000/account/signup/

- body: {
    "email": "abc@xyz.com",
    "password": "abc"
    }

- response: {
    "data": {
        "email": "abc@xyz.com",
        "password": "encoded_password"
    }
}


## User login
- url: http://localhost:8000/account/login/

- body: {
    "email": "abc@xyz.com",
    "password": "abc"
    }

- response: {
    "data": {
        "access_token": "eyJ.........",
        "refresh_token": "eyJ........"
    }
}


## User logout
- url: http://localhost:8000/account/logout/

- headers: {"Authorization": "Bearer <access_token>}

- response: {
    "data": "User logged out"
}


## Token refresh
- url: http://localhost:8000/account/refresh/

- body: {
    "refresh_token": "<refresh_token>"
}

- response: {
    "data":{
        "access_token": "<new_access_token>"
    }
}


## Chat account list
- url: http://localhost:8000/account/list/

- header: {"Authorization": "Bearer <access_token>}

- response: {
  "data": [
    {
      "id": 2,
      "email": "abc2@xyz.com"
    }
  ]
}

## Go to conversation with another user
- url: ws://localhost:8000/chat/<another_user_id>/messages/

- header: {"Authorization": "Bearer <access_token>}

- response: []

# Now you can send/recieve message in real time
- message: 'hi'

- response: [
    {
        "email": "abc@xyz.com",
        "message": "hi"
    }
]


## Running tests
- command: pytest
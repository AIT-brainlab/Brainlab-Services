# docker-jupyterhub
 
## Installation
1. Docker
2. pipenv and Python3.10

## Setup
```sh
pipenv install
```

## Creates list of user

### Dev mode

- go to ```secret/dev/student_id.txt``` 
```txt
{username} {base|custom}
...
```

- base: using the base image that we already prepared for them
- custom: needs to create Dockerfile by yourself and put it here ```./student-containers/{username}.Dockerfile```


## Creates the container templates

If we want to create a new user, please edit ```secret/{dev|prod}/student_id.txt```  and do this command.
```sh
pipenv run python generate-compose.py {cpu|gpu}
```

## Creates the container for each user

### Dev mode

```sh
pipenv run python docker-compose.py up --build -d
```

In case, you want to down all container
```sh
pipenv run python docker-compose.py down
```

## Happy Coding

### Dev mode
- go to ```localhost```
- make a user register
- do the login
- Enjoy!
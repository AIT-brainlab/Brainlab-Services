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

- go to ```secret/dev/users.txt``` 
- If the **subcontainer** is presented, the user volume would be shared throught all container.
```txt
{username}{-{subcontainer}|None} {base:cpu|base:gpu|custom:{username}-{tag}}
...
```

- base: using the base image that we already prepared for them
- custom: needs to create Dockerfile by yourself and put it here ```./user-custom-dockerfile/{username}-{tag}.Dockerfile```


## Creates the container templates

If we want to create a new user, please edit ```secret/{dev|prod}/users.txt```  and do this command.
```sh
pipenv run python generate-compose.py {dev|prod}
```

## Creates the container for each user


```sh
pipenv run python docker-compose.py {--dev|--prod|None} up --build -d
```
The default flat mode is ```--dev```.

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
- make a user register (needs to include the subcontainer if it exists)
- do the login
- Enjoy!
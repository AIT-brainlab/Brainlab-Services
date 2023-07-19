from components.logger import init_logger
from components.model import load_model 
import logging
import pickle
import os

import mlflow
import mlflow.pyfunc

from typing import Union
import uvicorn as uvicorn
from fastapi import FastAPI, APIRouter

# A bunch of global variable
MODEL_NAME:str = "mlflow-example"
STAGE:str = "Production"
MLFLOW_URL:str = "http://la.cs.ait.ac.th"
CACHE_FOLDER:str = os.path.join("/root","cache")
MODEL:mlflow.pyfunc.PyFuncModel

router = APIRouter(prefix="")


@router.get("/")
def get_root():
    return {"Hello": "World"}


@router.get("/items/{item_id}")
def get_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}



def create_app():
    fast_app = FastAPI()
    fast_app.include_router(router)
    return fast_app

def main():
    global MODEL
    # Init Logger
    init_logger(name="main", filename="main", path="/root/logs/", level=logging.DEBUG)
    logger = logging.getLogger(name="main")
    # Now prepare model
    mlflow.set_tracking_uri(MLFLOW_URL)
    MODEL = load_model(model_name=MODEL_NAME, stage=STAGE, cache_folder=CACHE_FOLDER)

    # init FastAPI
    app = create_app()
    logger.info("Start API")

    # RUN web server
    uvicorn.run(app=app, host="0.0.0.0", port=80, reload=True, workers=1, log_config="./uvicron-log.ini")

if __name__ == '__main__':
    main()
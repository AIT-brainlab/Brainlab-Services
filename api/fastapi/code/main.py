import mlflow
import mlflow.pyfunc
import pickle
import os


MODEL_NAME:str = "mlflow-example"
STAGE:str = "Production"
MLFLOW_URL:str = "http://la.cs.ait.ac.th"

CACHE_FOLDER:str = os.path.join("cache")

def load_model(model_name:str, stage:str) -> mlflow.pyfunc.PyFuncModel:
    model:mlflow.pyfunc.PyFuncModel = None # type:ignore

    # Check if cache
    model_path = os.path.join(CACHE_FOLDER,f"{model_name}_{stage}")
    if(os.path.exists(model_path) == True):
        with open(file=model_path, mode='rb') as file:
            model = pickle.load(file)

    else:
        # Load from mlflow registry
        model = mlflow.pyfunc.load_model(model_uri=f"models:/{model_name}/{stage}")
        # Save to cache
        with open(file=model_path, mode='wb') as file:
            pickle.dump(model, file)

    return model



mlflow.set_tracking_uri(MLFLOW_URL)
model = load_model(model_name=MODEL_NAME, stage=STAGE)




# pickle.d

# model.predict(data)

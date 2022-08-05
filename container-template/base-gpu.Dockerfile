FROM tensorflow/tensorflow:2.6.0


RUN apt update -y && apt upgrade -y
ENV DEBIAN_FRONTEND="noninteractive"

RUN apt install -yfm --no-install-recommends libgl1-mesa-glx libgtk2.0-dev

RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa


RUN apt install python3.10 -y
RUN apt install python3-pip -y
RUN apt install python3.10-distutils -y
RUN pip3 install pipenv

RUN pipenv --python 3.10

RUN pipenv install ipython==6.5.0
RUN pipenv install jupyterlab==3.4.4
RUN pipenv install torch==1.11.0 torchvision==0.12.0 torchaudio==0.11.0 --ignore-pipfile
RUN pipenv install 'pillow' --ignore-pipfile
RUN pipenv install opencv-python==4.6.0.66 --ignore-pipfile
RUN pipenv install "sklearn" --ignore-pipfile
RUN pipenv install "pandas" --ignore-pipfile
RUN pipenv install "seaborn" --ignore-pipfile
RUN pipenv install "matplotlib" --ignore-pipfile
RUN pipenv install "mypy==0.910" --ignore-pipfile
RUN pipenv install "pytest==6.2.5" --ignore-pipfile
RUN pipenv install "mne==0.23.4" --ignore-pipfile
RUN pipenv install "scipy==1.9.0" --ignore-pipfile





WORKDIR /home/container


# COPY ./jupyter_config /root/.jupyter
CMD tail -f /dev/null
# CMD pipenv run jupyter lab --ip='*' --port=8888 --no-browser  --allow-root --NotebookApp.token='' --NotebookApp.password=''
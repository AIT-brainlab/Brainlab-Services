FROM python:3.10.6
# I pick this version because my model was trained on this version.

# You do not need to expose 443.
# The TLS will be handled by `traefik`
EXPOSE 80

WORKDIR /root/code

RUN pip3 install --upgrade pip
# Specify the version so every build is consistent

# Let's install the FastAPI first.
RUN pip3 install fastapi==0.100.0
RUN pip3 install "uvicorn[standard]==0.23.1"
RUN pip3 install python-multipart==0.0.6

# Now you build your environment here
# Because I will fetch the model from mlflow, I will replicate the environment following what is specify in the requirements.txt
# http://la.cs.ait.ac.th/#/experiments/145195856694276689/runs/f74f23c4618e44388b47ade3f6d3563f
RUN pip3 install cffi==1.15.1
RUN pip3 install cloudpickle==2.2.1
RUN pip3 install defusedxml==0.7.1
RUN pip3 install dill==0.3.6
RUN pip3 install numpy==1.24.3
RUN pip3 install requests==2.31.0
RUN pip3 install torch==2.0.1
RUN pip3 install torchvision==0.15.2
RUN pip3 install tqdm==4.65.0
RUN pip3 install mlflow==2.4

# For Dev purpose
RUN pip3 install ipykernel

CMD tail -f /dev/null
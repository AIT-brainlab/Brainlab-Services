FROM python:3.10.5-buster
WORKDIR /home/src
EXPOSE 8000

RUN pip install "uvicorn[standard]"
RUN pip install fastapi==0.79.0
RUN pip install argon2-cffi==21.3.0
RUN pip install pymongo==4.2.0
RUN pip install mypy
RUN pip install pytest
RUN pip install requests
RUN pip install passlib==1.7.4


COPY ./src .

CMD uvicorn main:app --host 0.0.0.0 --reload
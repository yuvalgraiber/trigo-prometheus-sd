FROM python:3.14-slim

RUN python3 -m pip install flask==3.1.3
WORKDIR /code

COPY main.py main.py

ENTRYPOINT [ "python3", "main.py" ]

FROM python:3.7-alpine

WORKDIR /code
RUN pip install ckanapi
ADD . /code

EXPOSE 8000
CMD ["python3", "server.py"]
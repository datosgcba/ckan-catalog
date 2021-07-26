FROM python:3.9-buster

WORKDIR /code
RUN pip install ckanapi pandas xlsxwriter
ADD . /code

EXPOSE 8000
CMD ["python3", "server.py"]
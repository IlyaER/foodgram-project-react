FROM python:3.7-slim
LABEL author='ilyarog' version=1.01
RUN mkdir /app
COPY . /app
RUN pip3 install -r /app/requirements.txt --no-cache-dir
WORKDIR /app
CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]
FROM python:3.7-slim
LABEL author='ilyarog' version=1.02
RUN mkdir /app
COPY ./backend /app
COPY ./data/DejaVuSans.ttf /usr/share/fonts/truetype/
RUN pip3 install -r /app/requirements.txt --no-cache-dir
WORKDIR /app
CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]
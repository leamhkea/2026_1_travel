FROM python:3.9-slim
WORKDIR /app
COPY . /app
# Telling docker to not remember what is in the file (--no-cache-dir)
RUN pip install --no-cache-dir -r requirements.txt 
CMD flask run --host=0.0.0.0 --port=80 --debug --reload
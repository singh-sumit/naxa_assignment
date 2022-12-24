FROM python:3.10-slim-buster

WORKDIR /app

# COPY souce code
COPY . .

RUN pip3 install -r requirements/dev.txt

ENTRYPOINT ["sh", "docker-entrypoint.sh"]

# Execute on docker container while run
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
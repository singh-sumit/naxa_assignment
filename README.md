1. Create `SECRET_KEY`
```shell
openssl rand -hex 32
```

2. Run docker compose file
```shell
docker-compose up
```

3. Activate python virtualenv
4. Run `python manage.py runserver 8000`
5. Open up `http://127.0.0.1:8000/api/v1/docs` for **api docs**
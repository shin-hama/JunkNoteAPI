# JunkNoteAPI

This repository is API for Junk Note App.

## Getting Started

You can start running web server by docker with below command.

``` shell
> docker-compose build

> docker-compose up -d
```

If you wants to know the usage of api, you can access <http://localhost:8000/docs> that is api documentation based on [OpenAPI](https://github.com/OAI/OpenAPI-Specification).

## Development

### Migrate Database

Migration is used `alembic`. Please see [documentation](https://alembic.sqlalchemy.org/en/latest/) about detail usage.

Basic usage is next 3 steps.

1. Run and enter container
2. Edit `sqlalchemy` model
   - This is defined at [`app\models\models.py`](.\app\models\models.py)
3. Commit change with `alembic`
   - Command : `> poetry run alembic revision --autogenerate -m "comment"`
4. Run migration
   - Command : `> poetry run alembic upgrade head`

The migration is done every time the container is started, so you need to do it manually until commit the changes.

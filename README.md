# Project 
Dream Client

## Description

Flask API for Admin.

### Prerequisites

- Read [Software Development Cadence](https://www.notion.so/powerx/Software-Development-Cadence-1ae3ea74b4b04d949123205838380be6)
- Python 3.8
- Poetry
- Git

### Setup

```sh
# Clone this repo
git clone git@github.com:anujj86/dream_client.git
cd dream_client/anuj_jain

# Install dependencies
poetry install --no-root

# Activate the virtual environment (optional, but otherwise commands need to be prefixed with 'poetry run')
poetry shell
```

### Dependency management
All dependency changes and updates should be done via poetry. For details, see [poetry](https://python-poetry.org/docs/). If you change any dependencies, make sure [to commit the `poetry.lock` file](https://python-poetry.org/docs/basic-usage/#commit-your-poetrylock-file-to-version-control).

If any dependencies have changed in the remote repo, make sure to update your local environment via

```
git checkout main
git pull
poetry run pip uninstall -y gunicorn
poetry install --no-root
```

#### Making database schema updates

The `models` is responsible to define models, this project is responsible to handle database schema updates for the models.

- We have used flask-sqlalchemy as an ORM in the project. Since models files are being used by projects 
- to migrate to prod database, go to anuj_jain project, set CONFIG_TYPE=prod and for staging set CONFIG_TYPE=staging. In case on Linux OS, use export instead of set use export.
- run update.bat it will update common modules and migrate the changes to the corresponding database based on the CONFIG_TYPE environment variable set above. In case of Linux/Mac we can write corresponding sh file, make it executable and run it.
- ```poetry run flask db init``` (in case there is no migration folder inside anuj_jain project for that environment as currently we don't have it for prod)
- ```poetry run flask db migrate``` (after this one version file created inside the migration folder)
- ```poetry run upgrade ``` it will create the new table as well it will detech changes in table and upgrade it
- Please find the data in datbase folder and import it.

### Formatting and Linting

All code must be formatted and linted before committing and pushing to GitHub.

```sh
# Ensure everything is formatted correctly
poetry run black ./src ./*.py

# Ensure imports are sorted accordingly to PEP
poetry run isort .

# Check for runtime errors, syntax errors, and undefined names
poetry run flake8 ./src ./*.py --select=E9,F63,F7,F82 --show-source
```

### Testing

```sh
# Run unit tests
poetry run pytest

# Run the application (for integration tests, i.e. Swagger)
FLASK_ENV=staging poetry run flask run --host=127.0.0.1 --port=6000
```

## Run the Angular Application
- cd dream_client/anuj-jain-web
- Install the angular 13
- Install the node modules using command ```npm install```
- To run the angular project ```ng s```
- To create a build ```ng build```

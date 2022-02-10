# First-time setup
## Installing python
If you haven't already installed Python, you can install python from the following link. The team uses python 3.9.

https://www.python.org/downloads/

## Setting up your virtual environment
For testing and development, you will generally want to run in a python virtual environment.
This will allow you to run multiple python projects on the same machine without conflicting packages.

	python -m venv \<virtual_env_name\>

For example,

	python -m venv api_server_venv

## Installing requirements
The requirements.txt file contains the required python packages for the server to run

	pip install -r requirements.txt

## Installing dev requirements
The requirements-dev.txt file contains the required python packages for development and testing.

	pip install -r requirements-dev.txt

## pre-commit setup
Pre-commit is a python package that lets us run auto-formatters and static analysis tools on our code before all local 
commits.

	pre-commit install

## Installing postgres
You can download and run the installer for your development machine from here: https://www.postgresql.org/download/

We currently use postgres version 14.1.

During installation, you will be prompted for a password for the postgres super user.
You probably want have your default user be postgres with default password postgres since it is only running locally.

You will probably want to add the postgres bin directory to your path for easy access.

On a Windows machine, the path to the bin directory will look something like
	
	C:\Program Files\PostgreSQL\14\bin

## Configuring setup script
On Windows, configure the setup.bat file with the appropriate paths.

# Everytime setup
## Activating a python virtual environment
	/path/to/venv/Scripts/activate

For example
	
	./api_server_venv/Scripts/activate

## run setup
Run the setup script (setup.bat on Windows).

## Running postgres
Before running database or api tests, you will need to start postgres. You can start running postgres with the command

	postgres -p 5432 -D <path_to_data>

On a Windows machine, path_to_data is usually something like

	C:\Program Files\PostgreSQL\14\data

## Deactivating a python virtual environment
Once activated, you can deactivate your python virtual environment at any time with the command
	
	deactivate

# How to make a new database
If you need to start your database from scratch for testing, you can do the following

	F:\GitHub\Illu\api_server\database>psql -h localhost -p 5432 -U postgres  -f clean.sql
	F:\GitHub\Illu\api_server\database>psql -h localhost -p 5432 -U postgres  -f make.sql

# Developer Requirements before merging to main dev branch
## When making changes to requirements
When you make changes to requirements.txt, be sure to make the corresponding changes to .pre-commit-config.yaml

## When making changes to the database
Be sure to write an upgrade and downgrade sql script for the database. Be sure to also update the create script that 
generates a valid DB from scratch.

The create script is make.sql
The clean script is clean.sql

# Notes
## Running the server
	uvicorn --app-dir .\app main:app --reload

## Python Black
Python black is our auto-formatter. In the event that the standard formatting is obviously less readable,
you can turn off formatting for a block of code in the following way.

    # fmt: off
    np.array(
        [
            [1, 0, 0, 0],
            [0, -1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, -1],
        ]
    )
    # fmt: on

You can alter black's configuration in the pyproject.toml file.

## Flake8
Resolve all flake8 errors and warnings before submitting your pull request. If the particular flake8 suggestion is obviously worse,
You can disable a particular error for a line with a comment starting with "noqa". For example, if error F401 should be ignored...

    # noqa: F401

You can alter flake8's configuration in the .flake8 file.

## mypy
Mypy assists with static type analysis. If you must write code the violates static type analysis, you can disable mypy with the following
comment

    # type: ignore

You can alter mypy's configuration in the mypy.ini file. This can be helpful if you would like an import of a certain 
package to skip import checks everywhere.

More info here:
https://mypy.readthedocs.io/en/stable/index.html

More info on ignoring specific imports here:
https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-library-stubs-or-py-typed-marker
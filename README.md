# First-time setup
## Installing python
If you haven't already installed Python, you can install python from 

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

# Activating a python virtual environment
	/path/to/venv/Scripts/activate

For example
	
	./api_server_venv/Scripts/activate

# Deactivating a python virtual environment
Once activated, you can deactivate your python virtual environment at any time with the command
	
	deactivate

# Running postgres

# Python Black
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

# Flake8
Resolve all flake8 errors and warnings before submitting your pull request. If the particular flake8 suggestion is obviously worse,
You can disable a particular error for a line with a comment starting with "noqa". For example, if error F401 should be ignored...

    # noqa: F401

You can alter flake8's configuration in the .flake8 file.

# mypy
Mypy assists with static type analysis. If you must write code the violates static type analysis, you can disable mypy with the following
comment

    # type: ignore

You can alter mypy's configuration in the mypy.ini file.

More info here:
https://mypy.readthedocs.io/en/stable/index.html

# Making changes to requirements.txt
When you make changes to requirements.txt, be sure to make the corresponding changes to .pre-commit-config.yaml
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

# Making changes to requirements.txt
When you make changes to requirements.txt, be sure to make the corresponding changes to .pre-commit-config.yaml
### Pyenv

Make sure you have pyenv on your system, that you have followed the instructions from `pyenv init` and then in the project directory run:

```sh
pyenv install "3.10.6"
pyenv local "3.10.6"
```

Test that we have the correct python version:

```sh
python3 --version
realpath "$(which python3)"
```

The path returned should be something like: `/home/user/.pyenv/versions/3.10.6/bin/python3.10`

### venv

Create a virtual environment and install all the requirements:

```sh
python -m venv ".venv"
source .venv/bin/activate
pip install --upgrade pip
pip install -r "requirements.txt"
```

### Other

You will need a postgres DB. Adjust the connection string.

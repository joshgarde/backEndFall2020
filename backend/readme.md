# CSS Backend

[To the moon.](https://www.youtube.com/watch?v=YFMLHCMc91c)

## Installing Dependencies

All the project's dependencies are listed out in the `requirements.txt` file. To install, enter your venv and type the command:

```
pip3 install -r requirements.txt
```

## Configuring environment variables

Environment variables are handled via a `.env` file at the root of this directory. A sample `.env` file is provided in `.env.sample`. Copy the `.env.sample` file, rename it to `.env`, and change the variables to match your environment.

 **--- DO NOT check-in sensitive credentials to this repo ---**
 
## Building database tables

Database tables are built automagically by executing the `init_db.py` script.

```
python3 init_db.py
```

## Running tests

Unit tests are handled via the [python unittest library](https://docs.python.org/3/library/unittest.html). To run the tests, execute the `tests.py` file. Please ensure that the environment variables are set and the database tables are built before running tests.

```
python3 tests.py
```

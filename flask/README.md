# SEVERAL ROTATIONS Flask Web App

This directory contains the Flask web app version of `cli/several-rotations.py`.

1. Install prerequisites:

    - [CockroachDB](https://www.cockroachlabs.com/docs/stable/install-cockroachdb.html)
    - [virtualenv](https://virtualenv.pypa.io/en/latest/installation/)

2. Start CockroachDB:

    ```
    cockroach start --insecure
    ```

3. Use CockroachDB's [built-in SQL client](https://www.cockroachlabs.com/docs/stable/use-the-built-in-sql-client.html) to create the database schema:

    ```
    cockroach sql --insecure < schema.sql
    ```

4. Activate a virtualenv:

    ```
    python3 -m venv venv && . venv/bin/activate
    ```

5. Install [Flask](http://flask.pocoo.org/docs/1.0/installation) and [psycopg2](http://initd.org/psycopg/docs/install.html):

    ```
    pip install flask psycopg2
    ```

6. Start the app:

    ```
    FLASK_ENV=development python3 app.py
    ```

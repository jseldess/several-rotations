# SEVERAL ROTATIONS Flask Web App

This directory contains the Flask web app version of `cli/several-rotations.py`, deployed at [https://several-rotations.org](https://several-rotations.org). The site is the poem OUT, the last poem of the book [SEVERAL ROTATIONS](https://www.kenningeditions.com/shop/several-rotations/).

## Test locally

1. Install prerequisites:

    - [CockroachDB](https://www.cockroachlabs.com/docs/stable/install-cockroachdb.html)
    - [virtualenv](https://virtualenv.pypa.io/en/latest/installation/)

1. Start CockroachDB:

    ``` 
    cockroach start-single-node --insecure --listen-addr=localhost --background
    ```

1. As `root`, use CockroachDB's [built-in SQL client](https://www.cockroachlabs.com/docs/stable/use-the-built-in-sql-client.html) to create the database schema:

    ```
    cockroach sql --insecure < schema.sql
    ```

1. As `root`, use the built-in SQL client to create the `app` user and grant it privileges:

    ```
    cockroach sql --insecure --execute="CREATE USER app WITH PASSWORD '<your password>';"
    ```

    You can use the username and password to access the Admin UI later at `https://localhost:8080`.

    ```
    cockroach sql --insecure --execute="GRANT ALL ON DATABASE several_rotations TO app WITH GRANT OPTION;"
    ```

    ```
    cockroach sql --insecure --execute="GRANT ALL ON TABLE several_rotations.poems, several_rotations.state TO app WITH GRANT OPTION;"
    ```

1. Activate a virtualenv:

    ```
    python3 -m venv venv && . venv/bin/activate
    ```

1. Install requirements:

    ```
    pip install -r requirements.txt
    ```

1. In `app.py`, update the connection paramaters for local testing:

    ```
    conn = psycopg2.connect(
        database='several_rotations',
        user='app',
        sslmode='disable',
        port='26257',
        host='localhost',
        application_name='rotations'
    )
    ```

1. Start the app:

    ```
    export FLASK_APP=app
    ```

    ```
    export FLASK_ENV=development
    ```

    ```
    flask run
    ```

1. Once you're done testing, press CTRL + C to stop the app.

1. Get the process ID of CockroachDB:

    ```
    ps -ef | grep cockroach | grep -v grep
    ```

1. Stop CockroachDB:

    ```
    kill -TERM <process ID>
    ```

1. Deactivate the virtualenv:

    ```
    deactivate
    ```

1. Clean up:

    ```
    rm -rf cockroach-data venv
    ```
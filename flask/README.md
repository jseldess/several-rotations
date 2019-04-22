# SEVERAL ROTATIONS Flask Web App

This directory contains the Flask web app version of `cli/several-rotations.py`, deployed at [http://several-rotations.org](http://several-rotations.org). The site is the poem OUT, the last poem of the book SEVERAL ROTATIONS.

- [Start](#start)
- [Stop](#stop)
- [Restart](#restart)

## Start

1. Install prerequisites:

    - [CockroachDB](https://www.cockroachlabs.com/docs/stable/install-cockroachdb.html)
    - [virtualenv](https://virtualenv.pypa.io/en/latest/installation/)

2. Create security certificates:

    1. Create a directory for certificates and a safe directory for the CA key:

        ```
        mkdir certs my-safe-directory
        ```

    2. Create the CA (Certificate Authority) certificate and key pair:

        ```
        cockroach cert create-ca --certs-dir=certs --ca-key=my-safe-directory/ca.key
        ```

    3. Create the node certificate and key:

        ```
        cockroach cert create-node localhost $(hostname) --certs-dir=certs --ca-key=my-safe-directory/ca.key
        ```

    4. Create the client certificate and key, in this case for the `root` user and for the `app` user, which the app will use:

        ```
        cockroach cert create-client root --certs-dir=certs --ca-key=my-safe-directory/ca.key
        ```

        ```
        cockroach cert create-client app --certs-dir=certs --ca-key=my-safe-directory/ca.key
        ```    

3. Start CockroachDB:

    ```
    cockroach start --certs-dir=certs --listen-addr=localhost --join=localhost:26257 --background
    ```

    ```
    cockroach init --certs-dir=certs --host=localhost
    ```

4. As `root`, use CockroachDB's [built-in SQL client](https://www.cockroachlabs.com/docs/stable/use-the-built-in-sql-client.html) to create the database schema:

    ```
    cockroach sql --certs-dir=certs < rotations/schema.sql
    ```

5. As `root`, use the built-in SQL client to create the `app` user and grant it privileges:

    ```
    cockroach sql --certs-dir=certs --execute="CREATE USER app WITH PASSWORD '<your password>';"
    ```

    You can use the username and password to access the Admin UI later at `https://localhost:8080`.

    ```
    cockroach sql --certs-dir=certs --execute="GRANT ALL ON DATABASE several_rotations TO app;"
    ```

    ```
    cockroach sql --certs-dir=certs --execute="GRANT ALL ON TABLE several_rotations.poems, several_rotations.state TO app;"
    ```

6. Activate a virtualenv:

    ```
    python3 -m venv venv && . venv/bin/activate
    ```

7. Install [Flask](http://flask.pocoo.org/docs/1.0/installation) and [psycopg2](http://initd.org/psycopg/docs/install.html):

    ```
    pip install flask psycopg2
    ```

8. Start the app:

    ```
    export FLASK_APP=rotations
    ```

    ```
    export FLASK_ENV=development
    ```

    ```
    flask run
    ```

## Stop

1. Press CTRL + C to stop the app.

2. Stop CockroachDB:

    ```
    cockroach quit --certs-dir=certs --host=localhost
    ```

3. Deactivate the virtualenv:

    ```
    deactivate
    ```

## Restart

1. Restart CockroachDB:

    ```
    cockroach start --certs-dir=certs --listen-addr=localhost --join=localhost:26257 --background
    ```

2. Reactivate a virtualenv:

    ```
    . venv/bin/activate
    ```

3. Restart the app:

    ```
    export FLASK_APP=rotations
    ```

    ```
    export FLASK_ENV=development
    ```

    ```
    flask run
    ```

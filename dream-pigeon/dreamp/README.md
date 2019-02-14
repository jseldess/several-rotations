Run and initialize CockroachDB:
```
cockroach start --insecure
cockroach sql --insecure < statements.sql
```

Create virtual env, install requirements, and run flask app:
```
cd dreamp
chmod 755 setup.sh
./setup.sh
```
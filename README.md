django_postgres_vault
=====================

[![Latest PyPI version](https://img.shields.io/pypi/v/django_postgres_vault.svg "Latest PyPI version")](https://pypi.python.org/pypi/django_postgres_vault)

A simple Django database backend that allows rotating PostgreSQL access credentials via [HashiCorp Vault](https://www.vaultproject.io/)

Usage
-----

In your Django settings:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django_postgres_vault',
        'NAME': os.getenv('DB_NAME'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        'VAULT_ADDR': os.getenv('VAULT_ADDR'),
        'VAULT_TOKEN': os.getenv('VAULT_TOKEN'),
        'VAULT_ROLE_NAME': os.getenv('VAULT_ROLE_NAME'),
        'VAULT_DB_MOUNT_POINT': os.getenv('VAULT_DB_MOUNT_POINT'),
    }
}
```

Explanation of settings:

* `NAME`: The name of the Postgres database to connect to, as per Django standards.
* `HOST`: The host location of the Postgres database to connect to, as per Django standards.
* `PORT`: The host location port of the Postgres database to connect to, as per Django standards.
* `VAULT_ADDR`: The URL of the Vault server that will be providing rotating access credentials for the database. This is the same value as the `VAULT_ADDR` environment variable used by the Vault CLI command. Example: `https://vault-host-name:8200`
* `VAULT_DB_MOUNT_POINT`: The mount point of the database secrets engine in Vault. Default: `database`
* `VAULT_ROLE_NAME`: The name of a Vault database secrets engine role configured to provide Postgres credentials.
* `VAULT_TOKEN`: A Vault authentication token with read access to the database secrets engine role.

There are no `USER` or `PASSWORD` settings required because those will be dynamically provided by the Vault server. The settings can be provided, but will be ignored.

Installation
------------

`pip install django_postgres_vault`

### Requirements

* Django>=3.0
* psycopg2
* hvac

`Django` and `hvac` should be automatically installed by pip, but `psycopg2` will require manual installation. `psycopg2` or `psycopg2-binary` are both acceptable, but explicitly requiring either one in `setup.py` will make the library less usable for some users, so we defer on that front.

Compatibility
-------------

We officially support the most recent version of Django (3.0), as well as its supported Python versions (3.6, 3.7, 3.8). Other versions will most likely work, but there are no guarantees.

Licence
-------

MIT Licensed (see `LICENSE`)

Testing
-------

Testing is done using Tox and PyTest. A super-simple Dockerfile is provided to allow running Tox in an isolated container.



Authors
-------

`django_postgres_vault` was written by [Joe Ciskey](jciskey@inceptivecss.com).

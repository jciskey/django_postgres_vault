# Test that we can connect to a database using the new backend

import os
import hvac
from django_postgres_vault.base import DatabaseWrapper


def test_connection_functional():
    settings_dict = {
        'HOST': os.getenv('PG_HOST'),
        'PORT': os.getenv('PG_PORT'),
        'NAME': os.getenv('PG_DB_NAME'),
        'VAULT_DB_MOUNT_POINT': os.getenv('VAULT_DB_MOUNT_POINT', 'database'),
        'VAULT_ROLE_NAME': os.getenv('VAULT_ROLE_NAME'),
        'OPTIONS': {},
    }

    wrapper = DatabaseWrapper(settings_dict)

    conn_params = wrapper.get_connection_params()
    conn = wrapper.get_new_connection(conn_params)

    with conn.cursor() as cursor:
        cursor.execute("SELECT (%s %% 2) = 0 AS even", (10,))
        ret = cursor.fetchall()
        assert (ret == [(True,)]), "Invalid return value from test SELECT"

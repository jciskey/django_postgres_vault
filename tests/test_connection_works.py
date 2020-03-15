# Test that we can connect to a database using the new backend

import os
from django_postgres_vault.base import DatabaseWrapper


class TestDPVWrapperConnections:
    BASE_SETTINGS_DICT = {
        'HOST': os.getenv('PG_HOST'),
        'PORT': os.getenv('PG_PORT'),
        'NAME': os.getenv('PG_DB_NAME'),
        'VAULT_ADDR': os.getenv('VAULT_ADDR'),
        'VAULT_TOKEN': os.getenv('VAULT_TOKEN'),
        'VAULT_ROLE_NAME': os.getenv('VAULT_ROLE_NAME'),
        'VAULT_DB_MOUNT_POINT': os.getenv('VAULT_DB_MOUNT_POINT'),
        'OPTIONS': {},
    }

    def get_base_settings(self):
        return copy.deepcopy(self.BASE_SETTINGS_DICT)

    def run_test_connection_query(self, conn):
        """Helper function that runs a query against an
        active database connection to verify connectivity."""
        with conn.cursor() as cursor:
            cursor.execute("SELECT (%s %% 2) = 0 AS even", (10,))
            ret = cursor.fetchall()
            assert (ret == [(True,)]), "Invalid return value from test SELECT"

    def get_connection_from_settings(self, settings_dict):
        """Helper function that produces a connection
        using the provided settings dictionary."""
        wrapper = DatabaseWrapper(settings_dict)
        conn_params = wrapper.get_connection_params()
        conn = wrapper.get_new_connection(conn_params)
        return conn

    def run_connection_test(self, settings_dict):
        """Helper function to reduce repeated test code."""
        conn = self.get_connection_from_settings(settings_dict)
        self.run_test_connection_query(conn)

    def test_simple_connection_works(self):
        settings_dict = self.get_base_settings()
        self.run_connection_test(settings_dict)

    def test_connection_with_no_mount_point_setting_works(self):
        settings_dict = self.get_base_settings()
        del settings_dict['VAULT_DB_MOUNT_POINT']
        self.run_connection_test(settings_dict)

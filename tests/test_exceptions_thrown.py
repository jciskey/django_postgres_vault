

import os
import copy
import pytest

from django.core.exceptions import ImproperlyConfigured

from django_postgres_vault.base import DatabaseWrapper


class TestDPVWrapperExceptions:
    BASE_SETTINGS_DICT = {
        'HOST': os.getenv('PG_HOST'),
        'PORT': os.getenv('PG_PORT'),
        'NAME': os.getenv('PG_DB_NAME'),
        'VAULT_ADDR': os.getenv('VAULT_ADDR'),
        'VAULT_TOKEN': os.getenv('VAULT_TOKEN'),
        'VAULT_ROLE_NAME': os.getenv('VAULT_ROLE_NAME'),
        'VAULT_DB_MOUNT_POINT': os.getenv('VAULT_DB_MOUNT_POINT', 'database'),
        'OPTIONS': {},
    }

    def get_base_settings(self):
        return copy.deepcopy(self.BASE_SETTINGS_DICT)

    def test_vault_address_config_required(self):
        settings_dict = self.get_base_settings()

        del settings_dict['VAULT_ADDR']

        wrapper = DatabaseWrapper(settings_dict)

        with pytest.raises(ImproperlyConfigured):
            conn_params = wrapper.get_connection_params()




import os
import copy
import pytest

from django.core.exceptions import ImproperlyConfigured
from django.db import (
    InternalError,
    OperationalError,
)

from django_postgres_vault.base import DatabaseWrapper


class TestDPVWrapperExceptions:
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

    SEALED_VAULT_URL = os.getenv('SEALED_VAULT_URL')

    def get_base_settings(self):
        return copy.deepcopy(self.BASE_SETTINGS_DICT)

    def test_vault_address_config_required(self):
        settings_dict = self.get_base_settings()

        del settings_dict['VAULT_ADDR']

        wrapper = DatabaseWrapper(settings_dict)

        with pytest.raises(ImproperlyConfigured):
            conn_params = wrapper.get_connection_params()

    def test_vault_role_name_config_required(self):
        settings_dict = self.get_base_settings()

        del settings_dict['VAULT_ROLE_NAME']

        wrapper = DatabaseWrapper(settings_dict)

        with pytest.raises(ImproperlyConfigured):
            conn_params = wrapper.get_connection_params()

    def test_invalid_vault_token_throws_exception(self):
        settings_dict = self.get_base_settings()

        settings_dict['VAULT_TOKEN'] = '12345'

        wrapper = DatabaseWrapper(settings_dict)

        with pytest.raises(ImproperlyConfigured):
            conn_params = wrapper.get_connection_params()

    def test_invalid_vault_db_mount_point_throws_exception(self):
        settings_dict = self.get_base_settings()

        settings_dict['VAULT_DB_MOUNT_POINT'] = '12345'

        wrapper = DatabaseWrapper(settings_dict)

        with pytest.raises(InternalError):
            conn_params = wrapper.get_connection_params()

    def test_sealed_vault_address_throws_exception(self):
        settings_dict = self.get_base_settings()

        settings_dict['VAULT_ADDR'] = self.SEALED_VAULT_URL

        wrapper = DatabaseWrapper(settings_dict)

        with pytest.raises(OperationalError):
            conn_params = wrapper.get_connection_params()

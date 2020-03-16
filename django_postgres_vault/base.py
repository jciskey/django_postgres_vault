
import hvac
import requests

from django.core.exceptions import ImproperlyConfigured
from django.db import (
    InternalError,
    OperationalError,
)

from django.db.backends.postgresql import base


class DatabaseWrapper(base.DatabaseWrapper):

    DEFAULT_VAULT_DB_MOUNT_POINT = 'database'

    # Internal Vault client
    _hvac = None

    def _get_hvac_client(self):
        if self._hvac is None:
            # Build the hvac client and authenticate
            vault_url, vault_token = self._get_vault_login_credentials()

            if vault_url is None:
                raise ImproperlyConfigured(
                    "settings.DATABASES is improperly configured. "
                    "Please supply a valid Vault URL in VAULT_ADDR.")

            self._hvac = hvac.Client(url=vault_url)

            if vault_token is not None:
                self._hvac.token = vault_token
                try:
                    if not self._hvac.is_authenticated():
                        raise ImproperlyConfigured(
                            "settings.DATABASES is improperly configured. "
                            "Please supply a valid Vault token in VAULT_TOKEN.")
                except hvac.exceptions.VaultError as e:
                    msg = e.args[0]
                    raise OperationalError(msg)

        return self._hvac

    def _get_vault_login_credentials(self):
        settings_dict = self.settings_dict
        vault_url = settings_dict.get('VAULT_ADDR', None)
        vault_token = settings_dict.get('VAULT_TOKEN', None)
        return (vault_url, vault_token)

    def _get_database_credentials_from_vault(self):
        client = self._get_hvac_client()

        if not client.is_authenticated():
            raise RuntimeError("Not authenticated to Vault.")

        settings_dict = self.settings_dict

        vault_role_name = settings_dict.get('VAULT_ROLE_NAME', None)
        vault_db_mount_point = settings_dict.get('VAULT_DB_MOUNT_POINT', self.DEFAULT_VAULT_DB_MOUNT_POINT)
        if vault_db_mount_point is None:
            vault_db_mount_point = self.DEFAULT_VAULT_DB_MOUNT_POINT

        if vault_role_name is None:
            raise ImproperlyConfigured(
                "settings.DATABASES is improperly configured. "
                "Please supply a Vault role name in VAULT_ROLE_NAME.")

        params = {
            'name': vault_role_name,
            'mount_point': vault_db_mount_point,
        }

        try:
            creds = client.secrets.database.generate_credentials(**params)
        except requests.exceptions.MissingSchema as e:
            exc_msg = e.args[0]
            if exc_msg.startswith('Invalid URL') and ('No schema supplied' in exc_msg):
                raise ImproperlyConfigured(
                    "settings.DATABASES is improperly configured. "
                    "Please supply a valid Vault URL in VAULT_ADDR. "
                    "Did you forget your protocol schema? "
                    "e.g. 'http', 'https'")
            else:
                # If we don't know what happened,
                # re-raise the original exception
                raise e
        except hvac.exceptions.Forbidden as e:
            msg = e.args[0]
            raise InternalError(msg)
        except hvac.exceptions.VaultError as e:
            msg = e.args[0]
            raise OperationalError(msg)

        return creds

    def _get_username_password_from_vault(self):
        creds = self._get_database_credentials_from_vault()
        data = creds.get('data')
        username = data.get('username')
        password = data.get('password')
        return (username, password)

    def get_connection_params(self):
        # The Django Postgres backend expects these params,
        # and will error if they're not provided
        self.settings_dict['USER'] = ''
        self.settings_dict['PASSWORD'] = ''

        conn_params = super().get_connection_params()

        # We don't use these params, wipe them
        del self.settings_dict['USER']
        del self.settings_dict['PASSWORD']

        username, password = self._get_username_password_from_vault()

        conn_params['user'] = username
        conn_params['password'] = password

        return conn_params

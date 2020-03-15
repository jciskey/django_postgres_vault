from django.db.backends.postgresql import base


class DatabaseWrapper(base.DatabaseWrapper):

    def get_connection_params(self):
        conn_params = super().get_connection_params()

        return conn_params

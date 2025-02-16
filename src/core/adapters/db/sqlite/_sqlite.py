# inmemory
"""
        if config:
            database_url = ''.join([
                'postgresql+psycopg2://',
                f'{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}',
                '@',
                f'{config.POSTGRES_HOST}:{config.POSTGRES_PORT}',
                '/',
                config.POSTGRES_DB
            ])
            self.logger = logging.getLogger(f'postgres_{config.POSTGRES_DB}')
        else:
            database_url = 'sqlite:///:memory:'
            self.logger = logging.getLogger('sqlite_inmemory')
"""
import os


class Config:
    environment = os.environ.get('ENVIRONMENT')
    if environment == 'PROD':
        env_prefix = 'PROD'
    elif environment == 'DEV':
        env_prefix = 'DEV'
    else:
        env_prefix = 'QA'  # always QA

    # Database
    db_name = os.environ.get(F'{env_prefix}_DB_NAME')
    db_pass = os.environ.get(F'{env_prefix}_DB_PASS')
    db_host = os.environ.get(F'{env_prefix}_DB_HOST')
    db_user = os.environ.get(F'{env_prefix}_DB_USER')

    # secrets
    secret_key = os.environ.get(F'{env_prefix}_SECRET_KEY')

    # mongo
    mongo_db_name = os.environ.get(F'{env_prefix}_MONGO_DB_NAME')
    mongo_db_pass = os.environ.get(F'{env_prefix}_MONGO_DB_PASS')
    mongo_db_host = os.environ.get(F'{env_prefix}_MONGO_DB_HOST')
    mongo_db_user = os.environ.get(F'{env_prefix}_MONGO_DB_USER')

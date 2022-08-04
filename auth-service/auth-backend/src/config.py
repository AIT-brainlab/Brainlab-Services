import os
BASE_PATH = "/auth/api"
LASTEST_PASSWORD_ALG = "argon2-cffi"

DB_NAME = 'core-db'

USER_COLLECTION_NAME = 'users'
FORGOT_PASSWORD_TOKEN_COLLECTION_NAME = 'forget-password-token'
USER_SESSION_COLLECTION_NAME = 'user-session'

URL_RESET_EMAIL = os.environ['URL_RESET_EMAIL']
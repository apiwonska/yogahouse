import django_heroku
from decouple import config

DEBUG = config('DEBUG', default=False, cast=bool)
DEBUG=True
ALLOWED_HOSTS = ['yogahouse-ap.herokuapp.com']

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = 'eu-central-1'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'
AWS_STATIC_LOCATION = 'static'
DEFAULT_FILE_STORAGE = 'yogahouse.storages.MediaStorage'
AWS_S3_CUSTOM_DOMAIN = (
    f'{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com'
)
AWS_IS_GZIPPED = True
AWS_LOCATION = 'static'


django_heroku.settings(locals(), staticfiles=False)

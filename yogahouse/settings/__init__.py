from split_settings.tools import include, optional

base_settings = ['base.py',
                 'production.py',
                 optional('local.py')]

include(*base_settings)

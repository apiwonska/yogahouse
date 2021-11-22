from decouple import config


def ctx_dict(request):
    ctx = {}
    ctx['IMAGEKIT_URL'] = config('IMAGEKIT_URL')
    return ctx

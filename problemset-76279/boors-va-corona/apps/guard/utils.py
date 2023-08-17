from django.conf import settings
from django.urls import URLPattern, URLResolver, resolve

__all__ = ('get_client_ip', 'list_urls', 'list_views')


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def list_urls(lis, acc=None):
    if acc is None:
        acc = []
    if not lis:
        return
    l = lis[0]
    if isinstance(l, URLPattern):
        yield acc + [str(l.pattern)]
    elif isinstance(l, URLResolver):
        yield from list_urls(l.url_patterns, acc + [str(l.pattern)])
    yield from list_urls(lis[1:], acc)


def list_views():
    urlconf = __import__(settings.ROOT_URLCONF, {}, {}, [''])

    views = []
    for p in list_urls(urlconf.urlpatterns):
        path = '/' + ''.join(p)
        try:
            view, _, _ = resolve(path)
        except Exception as e:
            print(e)
        else:
            views.append((path, view.__name__))

    return views

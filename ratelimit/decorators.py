from __future__ import absolute_import

from functools import wraps
from django.shortcuts import HttpResponse

from ratelimit import ALL, UNSAFE
from ratelimit.exceptions import Ratelimited
from ratelimit.core import is_ratelimited

__all__ = ['ratelimit']


def ratelimit(group=None, key=None, rate=None, method=ALL, block=False):
    def decorator(fn):
        @wraps(fn)
        def _wrapped(request, *args, **kw):
            old_limited = getattr(request, 'limited', False)
            ratelimited = is_ratelimited(request=request, group=group, fn=fn,
                                         key=key, rate=rate, method=method,
                                         increment=True)
            request.limited = ratelimited or old_limited
            if ratelimited and block:
                # raise Ratelimited()
                request.session.flush()
                return HttpResponse("操作过于频繁，请稍后再试")
            return fn(request, *args, **kw)
        return _wrapped
    return decorator

def timelimit(group=None, key=None, rate=None, method=ALL, block=False):
    def decorator(fn):
        @wraps(fn)
        def _wrapped(request, *args, **kw):
            old_limited = getattr(request, 'limited', False)
            ratelimited = is_ratelimited(request=request, group=group, fn=fn,
                                         key=key, rate=rate, method=method,
                                         increment=True)
            request.limited = ratelimited or old_limited
            if ratelimited and block:
                request.session.flush()
                return HttpResponse("操作过于频繁，请稍后再试")
            return fn(request, *args, **kw)
        return _wrapped
    return decorator


ratelimit.ALL = ALL
ratelimit.UNSAFE = UNSAFE

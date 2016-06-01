#!/usr/bin/env python
# coding:utf-8


def args(*args, **kwargs):
    def _decorator(func):
        func.__dict__.setdefault('args', []).insert(0, (args, kwargs))
        return func
    return _decorator


def methods_of(obj):
    result = []
    for i in dir(obj):
        if callable(getattr(obj, i)) and not i.startswith('_'):
            result.append((i, getattr(obj, i)))
    return result


def func_args(func, match_args):
    fn_args = []
    for args, kwargs in getattr(func, 'args', []):
        arg = args[0]
        fn_args.append(getattr(match_args, arg))

    return fn_args

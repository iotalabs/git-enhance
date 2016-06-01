#!/usr/bin/env python
# coding:utf-8

import argparse


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
    

def parse_command(ENHANCES=[]):
    top_parser = argparse.ArgumentParser(prog='top')
    subparsers = top_parser.add_subparsers()

    for enhance in ENHANCES:

        command_object = ENHANCES[enhance]()
        command_parser = subparsers.add_parser(enhance)
        command_parser.set_defaults(command_object=command_object)
        command_subparsers = command_parser.add_subparsers(dest='action')
        for (action, action_fn) in methods_of(command_object):
            parser = command_subparsers.add_parser(action)
            action_kwargs = []
            for args, kwargs in getattr(action_fn, 'args', []):
                parser.add_argument(*args, **kwargs)

            parser.set_defaults(action_fn=action_fn)
            parser.set_defaults(action_kwargs=action_kwargs)

    match_args = top_parser.parse_args()
    fn = match_args.action_fn
    fn_args = func_args(fn, match_args)
    return fn, fn_args

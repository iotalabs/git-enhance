#!/usr/bin/env python
#coding:utf-8

import requests, commands, argparse
import sys


def args(*args,**kwargs):  
    def _decorator(func):  
        func.__dict__.setdefault('args', []).insert(0, (args,kwargs))  
        return func  
    return _decorator


class IssuesCommand(object):

    @args('state', nargs='?', default='opened', help='state support: [opened closed]')
    def list(self, state='opened'):
        api, token = gitlab_config()
        headers = {
            'PRIVATE-TOKEN': token
        }
        r = requests.request('GET', api + '/issues?state=' + state, headers=headers)
        print r.text
    

def gitlab_config():
    '''
    will return gitlab_api and gitlab_token
    '''
    gitlab_api   = commands.getstatusoutput('git config gitlab.api')
    gitlab_token = commands.getstatusoutput('git config gitlab.token')

    if gitlab_api[0] != 0:
        raise SystemExit('need config gitlab.api')
        
    if gitlab_token[0] != 0:
        raise SystemExit('need config gitlab.token')

    return gitlab_api[1], gitlab_token[1]
    

ENHANCES = {
    'issues': IssuesCommand,
}


def methods_of(obj):  
    result = []  
    for i in dir(obj):  
        if callable(getattr(obj, i)) and not i.startswith('_'):  
            result.append((i, getattr(obj, i)))  
    return result
    

def func_args(func, match_args):  
    fn_args = []  
    for args,kwargs in getattr(func, 'args', []):  
        arg = args[0]  
        fn_args.append(getattr(match_args, arg))  
  
    return fn_args  


if __name__ == '__main__':
    
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
    
    print "match_args:", match_args 
    fn = match_args.action_fn
    fn_args = func_args(fn, match_args)
    fn(*fn_args)
    # it works: python git-x.py issues list
    
    
    
    
    
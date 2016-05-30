#!/usr/bin/env python
#coding:utf-8

import requests, commands, argparse
import sys


class IssuesCommand(object):

    def list(self, state='open'):
        api, token = gitlab_config()
        print "api is %s and token is %s" % (api, token)
        headers = {
            'PRIVATE-TOKEN': token
        }
        r = requests.request('GET', api + '/issues?state=' + ''.join(state), headers=headers)
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
    match_args.action_fn(match_args.action_kwargs)
    
    # it works: python git-x.py issues list
    
    
    
    
    
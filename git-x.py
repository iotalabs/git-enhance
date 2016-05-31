#!/usr/bin/env python
# coding:utf-8

import requests
import commands
import argparse
from prettytable import PrettyTable
import re


def args(*args, **kwargs):
    def _decorator(func):
        func.__dict__.setdefault('args', []).insert(0, (args, kwargs))
        return func
    return _decorator


class IssuesCommand(object):

    @args('state', nargs='?', help='state support: [opened closed]')
    def list(self, state=''):
        api, token = gitlab_config()
        remote_url = current_remote()
        project_name = re.search(r'git.*/(.*)\.git', remote_url).group(1)
        headers = {
            'PRIVATE-TOKEN': token
        }
        
        _project = requests.request('GET',
                                    api + '/projects/search/' + project_name,
                                    headers=headers)
        project_id = _project.json()[0][u'id']
        r = requests.request('GET',
                             '%s/projects/%s/issues?state=%s' % (api, project_id, state),
                             headers=headers)
        print_issues(r.json())


def print_issues(issues):
    row = PrettyTable()
    row.field_names = ['issue id', 'name', 'state']
    for issue in issues:
        row.add_row(['#%d' % issue[u'iid'], issue[u'title'], issue[u'state']])
    print row


def current_remote():
    '''
    will return origin url
    '''
    gitlab_remote = commands.getstatusoutput('git remote get-url --all origin')
    if gitlab_remote[0] != 0:
        raise SystemExit(gitlab_remote[1])
    return gitlab_remote[1]


def gitlab_config():
    '''
    will return gitlab_api and gitlab_token
    '''
    gitlab_api = commands.getstatusoutput('git config gitlab.api')
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
    for args, kwargs in getattr(func, 'args', []):
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
    fn = match_args.action_fn
    fn_args = func_args(fn, match_args)
    fn(*fn_args)
    # it works: python git-x.py issues list

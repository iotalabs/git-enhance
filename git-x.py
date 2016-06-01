#!/usr/bin/env python
# coding:utf-8

import requests
import commands
import argparse
from prettytable import PrettyTable
import re
from gitlabConfig import GitlabConfig
from common import args, methods_of, func_args


class IssuesCommand(object):

    @args('state', nargs='?', help='state support: [opened closed]')
    def list(self, state=''):
        gitlab = GitlabConfig()
        remote_url = gitlab.current_remote()
        project_name = re.search(r'git.*/(.*)\.git', remote_url).group(1)
        headers = {
            'PRIVATE-TOKEN': gitlab.token
        }

        _project = requests.request('GET',
                                    gitlab.api + '/projects/search/' + project_name,
                                    headers=headers)
        project_id = _project.json()[0][u'id']
        r = requests.request('GET',
                             '%s/projects/%s/issues?state=%s' % (gitlab.api, project_id, state),
                             headers=headers)
        print_issues(r.json())


def print_issues(issues):
    row = PrettyTable()
    row.field_names = ['issue id', 'name', 'state']
    row.align = 'l'
    for issue in issues:
        row.add_row(['#%d' % issue[u'iid'], issue[u'title'], issue[u'state']])
    print row


ENHANCES = {
    'issues': IssuesCommand,
}


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

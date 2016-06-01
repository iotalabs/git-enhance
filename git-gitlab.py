#!/usr/bin/env python
# coding:utf-8

import requests
from prettytable import PrettyTable
import re
from gitlabConfig import GitlabConfig
from common import args, parse_command


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
    row.field_names = ['issue id', 'name', 'state', 'assignee', 'labels']
    row.align = 'l'
    for issue in issues:
        assignee = issue[u'assignee'] is not None and issue[u'assignee'][u'name'] or ''
        row.add_row(['#%d' % issue[u'iid'], issue[u'title'],
                     issue[u'state'], assignee, ','.join(issue[u'labels'])])
    print row


ENHANCES = {
    'issues': IssuesCommand,
}


if __name__ == '__main__':
    fn, fn_args = parse_command(ENHANCES)
    fn(*fn_args)
    # it works: python git-x.py issues list

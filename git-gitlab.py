#!/usr/bin/env python
# coding:utf-8

import requests
from prettytable import PrettyTable
import re
from helper import GitlabHelper
from api.gitlab_api import GitlabAPI
from common import args, parse_command

gitlabAPI = GitlabAPI()
gitlabHelper = GitlabHelper(gitlabAPI)


class IssuesCommand(object):

    @args('state', nargs='?', help='state support: [opened closed]')
    def list(self, state=''):

        project_id = gitlabHelper.current_project_id()
        _issues = gitlabAPI.project_issues(project_id)
        print_issues(_issues)

    @args('issue_id', nargs='?', help='issue id should be exists', type=int)
    def close(self, issue_id=''):
        project_id = gitlabHelper.current_project_id()
        _issues = gitlabAPI.project_issues(project_id)
        issue = filter(lambda issue: issue[u'iid'] == issue_id, _issues)[0]
        closed = gitlabAPI.project_issues_close(project_id=project_id, issue_id=issue[u'id'])
        print 'closed: %s' % (closed[u'state'] == u'closed' and 'Y' or 'N')


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

#!/usr/bin/env python
# coding:utf-8

import requests
import commands


class GitlabAPI(object):

    def __init__(self):
        _api = commands.getstatusoutput('git config gitlab.api')
        _token = commands.getstatusoutput('git config gitlab.token')

        if _api[0] != 0:
            raise SystemExit('need config gitlab.api')

        if _token[0] != 0:
            raise SystemExit('need config gitlab.token')

        self.api = _api[1]
        self.token = _token[1]
        self.headers = {
            'PRIVATE-TOKEN': self.token
        }

    def projects_search(self, keyword):
        r = requests.request('GET',
                             self.api + '/projects/search/' + keyword,
                             headers=self.headers)
        return r.json()

    def project_issues(self, project_id, state=''):
        r = requests.request('GET',
                             '%s/projects/%s/issues?state=%s' % (
                                 self.api, project_id, state),
                             headers=self.headers)
        return r.json()

    def project_issues_close(self, project_id='x', issue_id='x'):
        url = '%s/projects/%s/issues/%s?state_event=close' % (
            self.api, project_id, issue_id)
        r = requests.request('PUT', url, headers=self.headers)
        return r.json()

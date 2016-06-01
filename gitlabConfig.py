#!/usr/bin/env python
# coding:utf-8


import commands


class GitlabConfig(object):

    def __init__(self):
        _api = commands.getstatusoutput('git config gitlab.api')
        _token = commands.getstatusoutput('git config gitlab.token')

        if _api[0] != 0:
            raise SystemExit('need config gitlab.api')

        if _token[0] != 0:
            raise SystemExit('need config gitlab.token')

        self.api = _api[1]
        self.token = _token[1]

    def current_remote(self):
        '''
        will return origin url
        '''
        gitlab_remote = commands.getstatusoutput('git remote get-url --all origin')
        if gitlab_remote[0] != 0:
            raise SystemExit(gitlab_remote[1])
        return gitlab_remote[1]

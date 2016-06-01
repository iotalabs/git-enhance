#!/usr/bin/env python
# coding:utf-8


import commands
import re


class GitlabHelper(object):

    def __init__(self, gitlabAPI):
        super(GitlabHelper, self).__init__()
        self.gitlabAPI = gitlabAPI

    def current_remote(self):
        '''
        will return origin url
        '''
        _remote = commands.getstatusoutput('git remote get-url --all origin')
        if _remote[0] != 0:
            raise SystemExit(_remote[1])
        return _remote[1]

    def current_project_id(self):
        _id = commands.getstatusoutput('git config gitlab.projectId')

        if _id[0] == 0:
            return _id[1]

        remote_url = self.current_remote()
        project_name = re.search(r'git.*/(.*)\.git', remote_url).group(1)
        projects = self.gitlabAPI.projects_search(project_name)

        for pro in projects:
            if pro[u'ssh_url_to_repo'] == remote_url:
                commands.getstatusoutput('git config gitlab.projectId %d' % pro[u'id'])
                return pro[u'id']

        raise SystemExit("Failed to get project id")

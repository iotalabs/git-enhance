# Git Enhance

Git命令行小工具

## 安装

```
brew tap iotalabs/homebrew
brew install git-jenkins
brew install git-gitlab
```

## 升级

```
brew update
brew upgrade git-jenkins
brew upgrade git-gitlab
```

## git-jenkins

Jenkins命令行小工具

### 参数配置

从git config

- git config jenkins.url http://jenkins_url
- git config jenkins.token TOKEN
- git config jenkins.login your@mail.com

从环境变量

- export JENKINS_URL=http://jenkins_url
- export JENKINS_TOKEN=TOKEN
- export JENKINS_LOGIN=your@mail.com

### 子命令

- git jenkins list                  获取项目列表
- git jenkins generate              生成创建项目的配置文件
- git jenkins credentials <domain>  获取Jenkins的Git远程认证信息
- git jenkins create <project>      创建一个项目
- git jenkins build <project>       启动构建任务
- git jenkins log <project>         查看构建日志

### 配置文件

一般配置文件名为 `config.xml`

在Git项目下，运行 `git jenkins generate`，
会获取到 `git remote.origin.url` 作为 `hudson.plugins.git.UserRemoteConfig` 的 `url` 地址。
并且获取当前的branch为 `hudson.plugins.git.BranchSpec` 的 `branch` 。

用户需要填写的变量

- *YOUR GIT REMOTE CREDENTIALS* 可以通过 `git jenkins credentials` 获得
- *YOUR SHELL COMMAND* 需要构建的运行脚本

这个模板是仅提供最基本的功能，可以完全重写以符合自己的需求。

示例

```
<?xml version='1.0' encoding='UTF-8'?>
<project>
  <actions/>
  <description></description>
  <keepDependencies>false</keepDependencies>
  <properties/>
  <scm class="hudson.plugins.git.GitSCM" plugin="git@2.4.4">
    <configVersion>2</configVersion>
    <userRemoteConfigs>
      <hudson.plugins.git.UserRemoteConfig>
        <url>git@github.com:ygmpkk/git-jenkins.git</url>
        <credentialsId>9b846252-8d17-45e3-9da2-10537b009c9e</credentialsId>
      </hudson.plugins.git.UserRemoteConfig>
    </userRemoteConfigs>
    <branches>
      <hudson.plugins.git.BranchSpec>
        <name>develop</name>
      </hudson.plugins.git.BranchSpec>
    </branches>
    <doGenerateSubmoduleConfigurations>false</doGenerateSubmoduleConfigurations>
    <submoduleCfg class="list"/>
    <extensions/>
  </scm>
  <canRoam>true</canRoam>
  <disabled>false</disabled>
  <blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding>
  <blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>
  <triggers/>
  <concurrentBuild>false</concurrentBuild>
  <builders>
    <hudson.tasks.Shell>
      <command>set
VERSION=`date +%Y%m%d`
sh pkg.sh $GIT_BRANCH $VERSION.$BUILD_ID
      </command>
    </hudson.tasks.Shell>
  </builders>
  <publishers/>
  <buildWrappers/>
</project>
```

### 演示步骤

```
> git config jenkins.url http://jenkins_url:8080

> git jenkins credentials

TITLE:
Global credentials (unrestricted)

DESCRIPTION:
Credentials that should be available irrespective of domain specification to requirements matching.

NAME                          KEY
jenkins                       xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

> git jenkins generate > config.xml
> cat config.xml

<?xml version='1.0' encoding='UTF-8'?>
<project>
  <actions/>
  <description></description>
  <keepDependencies>false</keepDependencies>
  <properties/>
  <scm class="hudson.plugins.git.GitSCM" plugin="git@2.4.4">
    <configVersion>2</configVersion>
    <userRemoteConfigs>
      <hudson.plugins.git.UserRemoteConfig>
        <url>git@github.com:ygmpkk/git-jenkins.git</url>
        <credentialsId>YOUR GIT REMOTE CREDENTIALS</credentialsId>
      </hudson.plugins.git.UserRemoteConfig>
    </userRemoteConfigs>
    <branches>
      <hudson.plugins.git.BranchSpec>
        <name>master</name>
      </hudson.plugins.git.BranchSpec>
    </branches>
    <doGenerateSubmoduleConfigurations>false</doGenerateSubmoduleConfigurations>
    <submoduleCfg class="list"/>
    <extensions/>
  </scm>
  <canRoam>true</canRoam>
  <disabled>false</disabled>
  <blockBuildWhenDownstreamBuilding>false</blockBuildWhenDownstreamBuilding>
  <blockBuildWhenUpstreamBuilding>false</blockBuildWhenUpstreamBuilding>
  <triggers/>
  <concurrentBuild>false</concurrentBuild>
  <builders>
    <hudson.tasks.Shell>
      <command>
        YOUR SHELL COMMAND
      </command>
    </hudson.tasks.Shell>
  </builders>
  <publishers/>
  <buildWrappers/>
</project>

> Youu should replace YOUR GIT REMOTE CREDENTIALS and YOUR SHELL COMMAND

> git jenkins create test config.xml

Jenkins: Create job test
SUCCESS

> git jenkins list

JOBS:
NAME                       STATUS
test                       NOTBUILT

VIEWS:
NAME         URL
All          http://jenkins_url:8080/
```

## git-gitlab

Gitlab命令行工具

### 参数配置

从git config

- git config gitlab.url http://gitlab_url
- git config gitlab.token TOKEN

从环境变量

- export GITLAB_SCHEMA=http
- export GITLAB_TOKEN=TOKEN

> 工具会默认从git config读取remote的origin.url配置,
> 如果是ssh地址，会自动转换成http[s]地址。

### 子命令

#### Users

- git gitlab user list      获取用户列表

#### Labels

- git gitlab label list     获取Label列表

#### Issues

- git gitlab issue list     获取Issue列表
- git gitlab issue create   新建Issue
- git gitlab issue update   更新Issue
- git gitlab issue delete   删除Issue
- git gitlab issue close    关闭Issue
- git gitlab issue open     打开Issue
- git gitlab issue comment  Issue留言

#### Comments

- git gitlab comment list <issue>           获取Comment列表
- git gitlab comment reply <issue> <user>   回复Comment

#### Merge Requests

- git gitlab merge list                                                         获取Merge Request列表
- git gitlab merge create \<source branch\> \<target branch\> \<assignee\> \<title\>    新建Merge Request
- git gitlab merge update \<merge id\> \<target branch\> \<assignee\> \<title\>         更新Merge Request
- git gitlab merge accept \<merge id\>                                            接受Merge Request
- git gitlab merge get summary \<merge id\>                                       获取Merge Request信息
- git gitlab merge get commit \<merge id\>                                        获取Merge Request Comment信息
- git gitlab merge get change \<merge id\>                                        获取Merge Request Change信息
- git gitlab merge get issue \<merge id\>                                         获取Merge Request Issue列表


# License

The MIT License (MIT)

Copyright (c) 2016 Iota Labs

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

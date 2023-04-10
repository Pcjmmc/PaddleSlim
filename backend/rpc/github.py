# -*- coding:utf8 -*-
import asyncio
import os
import sys

import aiohttp

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from ce_web.settings.common import RPC_SETTINGS, PROXY
from utils.change_time import stmp_by_date

from rpc.base import BaseRpc

PADDLE_GIT_GATEWAY = RPC_SETTINGS['github_paddle']['gateway']
PADDLE_GIT_USER = RPC_SETTINGS['github_paddle']['username']
PADDLE_GIT_PASSD = RPC_SETTINGS['github_paddle']['token']

class GetTags(BaseRpc):
    """
    修改用户名
    """
    method = 'get'
    gateway = PADDLE_GIT_GATEWAY
    api = 'tags'
    proxy = PROXY
    auth = aiohttp.BasicAuth(
        login=PADDLE_GIT_USER,
        password=PADDLE_GIT_PASSD,
        encoding='utf-8'
    )

    async def get_latest_tag_info(self, **kwargs):
        tag_list = await self.get_data(**kwargs)
        tag_info = tag_list[0] if tag_list else {}
        latest_tag_info = {
            "name": tag_info.get("name"), 
            "commit": tag_info.get("commit")
        }
        return latest_tag_info

    async def get_data(self, **kwargs):
        result = await self.is_valid()
        if result and str(self._status == '200'):
            return self.response_json
        return {}

class GetBranches(BaseRpc):
    """
    修改用户名
    """
    method = 'get'
    gateway = PADDLE_GIT_GATEWAY
    api = 'branches/{branch}'
    proxy = PROXY
    auth = aiohttp.BasicAuth(
        login=PADDLE_GIT_USER,
        password=PADDLE_GIT_PASSD, 
        encoding='utf-8'
    )

    def process_api(self, **kwargs):
        self.api = self.api.format(**kwargs)

    async def get_commit_info_by_branch(self, **kwargs):
        # 根据branch分支获取开始集中测试起始的时间&commit
        self.process_api(**kwargs)
        result = await self.get_data()
        commit = result.get("commit") if result else {}
        commit_id = commit.get("sha") if commit else ''
        commit = commit.get("commit") if commit else {}
        date = commit.get("committer", {}).get("date")
        return {"commit": commit_id , "time": date}

    async def get_data(self, **kwargs):
        result = await self.is_valid()
        if result and str(self._status == '200'):
            return self.response_json
        return {}


class GetCommit(BaseRpc):
    """
    根据指定commit回去相应的创建时间
    """
    method = 'get'
    gateway = PADDLE_GIT_GATEWAY
    api = 'commits/{commit}'
    proxy = PROXY
    auth = aiohttp.BasicAuth(
        login=PADDLE_GIT_USER,
        password=PADDLE_GIT_PASSD, 
        encoding='utf-8'
    )

    def process_api(self, **kwargs):
        self.api = self.api.format(**kwargs)

    async def get_commit_info(self, **kwargs):
        # 根据branch分支获取开始集中测试起始的时间&commit
        self.process_api(**kwargs)
        result = await self.get_data()
        commit = result.get('commit') if result else {}
        return commit.get('committer') if commit else {}

    async def get_data(self, **kwargs):
        result = await self.is_valid()
        print(result)
        if result and str(self._status == '200'):
            return self.response_json
        return {}

class GetCommits(BaseRpc):
    """
    根据分支或者tag来获取 rd 提交的commits列表
    """
    method = 'get'
    gateway = PADDLE_GIT_GATEWAY
    api = 'commits'
    proxy = PROXY
    auth = aiohttp.BasicAuth(
        login=PADDLE_GIT_USER,
        password=PADDLE_GIT_PASSD, 
        encoding='utf-8'
    )
    headers = {"Accept": "application/vnd.github.v3+json"}
    params_keys = (
        {"key": "page", "type": int, "required": True},
        {"key": "per_page", "type": int,  "required": True},
        {"key": "sha", "type": str,  "required": True},
    )

    async def get_commit_list(self, **kwargs):
        res = await self.get_data()
        commits = []
        for item in res:
            commit = item.get('sha')
            commiter = item.get('commit', {})
            author = commiter.get("author", {})
            commit_time = author.get("date", '')
            commits.append({"commit": commit, "commit_time": commit_time})
        return commits

    async def get_data(self, **kwargs):
        result = await self.is_valid()
        if result and str(self._status == '200'):
            return self.response_json
        return {}

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    # latest_tag = loop.run_until_complete(GetTags().get_latest_tag_info())
    # # 根据commit来获取
    # print("latest tag info is", latest_tag)
    # commit = latest_tag.get("commit", {}).get("sha")
    # print("tag  latest commit is", commit)
    commit_info = loop.run_until_complete(GetCommit().get_commit_info(**{"commit": '590b4dbcdd989324089ce43c22ef151c746c92a3'}))
    print("tag  latest commit info  is", commit_info)
    begin_time = str(commit_info['date'])
    begin_time = stmp_by_date(begin_time, fmt="%Y-%m-%dT%H:%M:%SZ")
    # 时间戳+8
    begin_time = begin_time + 28800
    print(begin_time)
    # git_branches = loop.run_until_complete(GetBranches().get_commit_info_by_branch(**{"branch": "release/2.2"}))
    # commits = loop.run_until_complete(GetCommits({'page': 1, "per_page": 3, "sha": "release/2.2"}).get_commit_list())
    # print("branches  latest commit info is", commits)

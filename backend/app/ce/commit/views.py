# !/usr/bin/env python3
"""
负责commit相关crud等操作
"""
# encoding=utf-8
import asyncio
import datetime
import json
import time

from ce_web.settings.scenes import scenes_dict
from models.release_version import CeReleaseVersion
from rpc.github import GetCommits
from services.tasks import TaskBuildInfo, TasksInfo

from views.auth_view import AuthCheck
from views.base_view import MABaseView


class CommitsManage(MABaseView):

    auth_class = AuthCheck

    async def get(self, **kwargs):
        """
        调用基类的get方法
        """
        return await super().get(**kwargs)

    async def get_data(self, **kwargs):
        """
        根据具体的版本信息，则将改版本的rd的commit列表返回
        根据version信息，通过github想rd提交的commit信息罗列出来
        params: verison 版本信息
        params: page 分页
        params: pagesize 每页大小
        """
        commits = []
        version = kwargs.get("version")
        page = kwargs.get("page", 1)
        per_page = kwargs.get("pagesize", 30)
        # develop的特殊处理
        if version == "develop":
            sha = version
            commits = await GetCommits(
                {'page': page, "per_page": per_page, "sha": sha}
            ).get_commit_list() 
        else:
            # 分页获取
            res = await CeReleaseVersion().aio_get_object(**{"name": version})
            if res:
                if res.activated:
                    sha = res.branch
                else:
                    sha = res.end_commit
                commits = await GetCommits(
                    {'page': page, "per_page": per_page, "sha": sha}
                ).get_commit_list()

        commit_list = [item.get("commit") for item in commits]
        commits_info = await self.check_commit(commit_list)
        for item in commits:
            commit = item.get("commit")
            item["checked"] = True if commits_info.get(commit) else False
        return len(commits), commits

    async def check_commit(self, commits):
        """
        check commit 是否QA回归过
        """
        # 获取覆盖此commit的任务
        commits_info = await TaskBuildInfo.check_commit(commits)
        return commits_info

class CommitDetailManage(MABaseView):

    auth_class = AuthCheck
    
    async def get(self, **kwargs):
        """
        调用基类的get方法
        """
        return await super().get(**kwargs)

    async def get_data(self, **kwargs):
        """
        根据具体的commit，则返回具体的commit的覆盖信息
        """
        commit_data = []
        need_backup = False
        commit = kwargs.get("commit")
        version = kwargs.get("version")
        if commit and version:
            if version.startswith("release"):
                step = "release"
            else:
                step = version
                need_backup = False if version == "develop" else True
            # 根据release 的细腻来查询,改接口是负责release的，故step=release
            all_release_task = await TasksInfo.get_all_task_info_by_filter(
                step=step, backup=need_backup, version=version
            )
            # 查询到来全量任务
            tids = [item.get("id") for item in all_release_task]
            # 获取覆盖此commit的任务
            build_info = await TaskBuildInfo.get_task_status_by_tids_and_commit(tids, commit)
            # 真正跑过改commit的任务：
            real_tids = [key for key in build_info]
            # 过滤一遍all_release_task
            all_release_task = [
                item for item in all_release_task if item.get("id") in real_tids]
            temp_data = [{
                "tid": item["id"],
                "tname": item["tname"],
                "description": item["description"],
                "system": item["system"],
                "secondary_type": item["secondary_type"],
                "reponame": item.get("reponame"),
                "task_type": item["task_type"]} for item in all_release_task]
            for item in temp_data:
                tid = item["tid"]
                item["status"] = build_info[tid].get("status")
                item["exit_code"] = build_info[tid].get("exit_code")
                item["build_id"] = build_info[tid].get("build_id")
                item["commit_id"] = build_info[tid].get("commit_id")
                item["created"] = build_info[tid].get("created")
                item["branch"] = build_info[tid].get("branch")
                item["repo"] = build_info[tid].get("repo")
                artifact_url = build_info[tid].get("artifact_url")
                if artifact_url:
                    try:
                        item["artifact_url"] = json.loads(artifact_url)
                    except:
                        item["artifact_url"] = []
            # 先获取到所有的seneces,origin_scenes主要用来维持顺序
            origin_scenes = [item for item in scenes_dict]
            scenes = set()
            for item in all_release_task:
                scenes.add(item.get("task_type"))
            scenes = list(scenes)
            scenes = [item for item in origin_scenes if item in scenes]
            commit_data = {sen: list() for sen in scenes if sen != "lite"}
            for item in temp_data:
                sen = item["task_type"]
                commit_data[sen].append(item)
            commit_data = [{"scenes": scenes_dict[key], "data": val}
                           for key, val in commit_data.items()]

        return len(commit_data), commit_data

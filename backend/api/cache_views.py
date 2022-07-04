"""
提供api负责单个任务最新的一次build 结果保存
"""
# encoding: utf-8
import asyncio
import json

from api.cache import BuildCacheBase
from views.base_view import MABaseView


class BuildCacheView(MABaseView):
    """
    更新缓存接口
    """

    async def post(self, **kwargs):
        return await super().post(**kwargs)

    async def post_data(self, **kwargs):
        """
        缓存每个任务最新的一次，key是任务的唯一id; 
        db的id与build_type_id 都是唯一的；且一一对映，故这里用tid
        """
        tid = kwargs.get("tid")
        branch = kwargs.get("branch") or ""
        branch = branch.strip()
        branch = branch.split("/")[0]
        cache_branch = None
        # 只有是回归release/dev的才更新缓存；其他的不更新
        if branch in ["release", "develop"]:
            cache_branch = branch
        if tid and cache_branch:
            # 删除已经存在的key；不支持追究，因为每次都是完整存入
            await BuildCacheBase.delete_keys(tid, cache_branch)
            await BuildCacheBase.set_multi(tid, cache_branch, data=kwargs)

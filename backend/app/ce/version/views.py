# encoding: utf-8
"""
负责集测开始和集测结束的version控制
"""
import asyncio
import time

from models.release_version import CeReleaseVersion
from rpc.github import GetCommit
from services.menu import update_menu
from utils.change_time import stmp_by_date
from exception import HTTP400Error
from views.base_view import MABaseView


class CreateRVersion(MABaseView):

    async def get(self, **kwargs):
        """
        调用子类的获取数据方法
        """
        return await super().get(**kwargs)

    async def get_data(self, **kwargs):
        # 根据查询需求将版本的相关信息以及steps信息返回到前端
        """
        返回当前激活的发版计划
        """
        # 创建完需要更新下menu
        result = await CeReleaseVersion.aio_get_object(**{"activated": 1})
        # 将对象转换成字典
        if result:
            result = [{column: value for column, value in result.items()}]
        else:
            result = []
        return 1, result


    async def post(self, **kwargs):
        """
        调用基类的post方法
        """
        return await super().post(**kwargs)

    async def post_data(self, **kwargs):
        # 根据参数初始化一次发版记录是
        """
        创建发版计划: activated的,
        params: 
            branch: 分支
            tag: 计划版版
            begin_commit: 集测开始commit
        """
        begin_commit = kwargs.get("begin_commit")
        try:
            commit_info = await GetCommit().get_commit_info(**{"commit": begin_commit})
            begin_time = str(commit_info['date'])
            begin_time = stmp_by_date(begin_time, fmt="%Y-%m-%dT%H:%M:%SZ")
        except:
            raise HTTP400Error("commit is incorrect")
        validated_data = {
            "name": kwargs.get("branch"),
            "branch": kwargs.get("branch"),
            "tag": kwargs.get("tag"),
            "begin_commit": begin_commit,
            "begin_time": begin_time,
            "activated": 1,
        }
        await CeReleaseVersion.aio_insert(validated_data=validated_data)
        await update_menu()

    async def put(self, **kwargs):
        """
        就是展示最新激活的那个发版计划
        打tag之后，表示集测结束，需要将真正的tag和end_time、end_commit更新进去
        更新name、end_time, end_commit：集测结束的commit
        正式的tag
        激活状态等信息
        更新菜单数据
        """
        return await super().put(**kwargs)


    async def put_data(self, **kwargs):
        """
        更新记录; 主要更新tag名以及
        end_time、 end_commit、updated、activated、 name等
        """
        _id = kwargs.get("id")
        end_commit = kwargs.get("end_commit")
        try:
            commit_info = await GetCommit().get_commit_info(**{"commit": end_commit})
            end_time = str(commit_info['date'])
            end_time = stmp_by_date(end_time, fmt="%Y-%m-%dT%H:%M:%SZ")
        except:
            raise HTTP400Error("commit is incorrect")
        validated_data = {
            "name": kwargs.get("tag"),
            "end_commit": end_commit,
            "end_time": end_time,
            "activated": 0,
            "updated": int(time.time())
        }
        await CeReleaseVersion.aio_update(
            validated_data=validated_data, params_data={"id": _id}
        )
        await update_menu()

    async def delete(self, **kwargs):
        """
        调用子类的删除方法
        """
        return await super().delete(**kwargs)

    async def delete_data(self, **kwargs):
        """
        删除发版计划；重新建立
        """
        await CeReleaseVersion.aio_delete(params_data=kwargs)
        await update_menu()

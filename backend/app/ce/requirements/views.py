# !/usr/bin/env python3
# encoding=utf-8
import asyncio
import datetime
import json
import time

from ce_web.settings.common import (
    RPC_SETTINGS, TC_BASE_URL, XLY_BASE_URL, XLY_BASE_URL2
)
from ce_web.settings.scenes import back_dict, inner_dict, scenes_dict, selects
from models.icafe import CeIcafe
from models.project import Project
from rpc.icafe import CreateCard, GetCards, ModifyCardStatus

from views.base_view import MABaseView

PADDLE_ICAFE_USER = RPC_SETTINGS['paddle_icafe']['username']
PADDLE_ICAFE_PASSD = RPC_SETTINGS['paddle_icafe']['password']
baseUrl = "https://console.cloud.baidu-int.com/devops/icafe/issue/{space}-{sequence}/show"


class ManageIcafe(MABaseView):

    async def get(self, **kwargs):
        """
        调用基类的get方法
        """
        return await super().get(**kwargs)

    async def get_data(self, **kwargs):
        """
        响应请求, 实现获取数据逻辑, 并返回符合查询条件的数据
        """
        # 获取所有的处于新建、开发中、开发完成的卡片
        # 按照最后修改时间进行时间窗口筛选
        page = kwargs.get("page")
        if not page:
           page = 1
        page_num = kwargs.get("page_num")
        if not page_num:
           page_num = 20
        begin_time = kwargs.get("begin_time")
        end_time = kwargs.get('end_time')
        if not begin_time and not end_time:
            today = datetime.date.today()
            end_time = str(today)
            begin_time = str(today - datetime.timedelta(days=14))  
        if begin_time and not end_time:
            today = datetime.date.today()
            end_time = str(today)
        if not begin_time and end_time:
            end_time_date = datetime.datetime.strptime(end_time, '%Y-%m-%d') 
            begin_time = str(end_time_date - datetime.timedelta(days=14))
        print("begin_time =", begin_time, "end_time=", end_time)
        rd = kwargs.get('rd')
        qa = kwargs.get('qa')
        #story和任务后续去掉，只保留Task和bug
        iql = "流程状态 in (新建,开发中,开发完成) AND 类型 in (Task,Bug,Story,任务) AND 最后修改时间 > {} AND 最后修改时间 < {}".format(begin_time, end_time)
        if rd:
           sub_iql = " AND 负责人 in ({})".format(rd)
           iql = iql + sub_iql
        if qa:
           sub_iql = " AND qa负责人 in ({})".format(qa)
           iql = iql + sub_iql
        return await get_cards_by_filter(page, page_num, iql)

    async def post(self, **kwargs):
        """
        调用基类的get方法
        """
        return await super().post(**kwargs)

    async def post_data(self, **kwargs):
        """
        响应请求, 实现创建icafe卡片
        """
        # 新建卡片
        print("新建卡片")
        fields = kwargs.get("fields")
        # repo和产品保持一致（这里填充，减少后续卡片状态修改报错）
        repo = fields.get("repo")
        icafe_info = {
            "title": fields.get("title"),
            #TODO 创建卡片类型是否需要放开，暂时默认为Task
            "type": "Task",
            "detail": fields.get("description"),
            "fields": {},
            "负责人": fields.get("rd_owner"),
            "RD负责人": fields.get("rd_owner"),
            #TODO 创建卡片是否需要指定qa？
            "qa负责人": fields.get("qa_owner")
        }
        icafe_info["fields"] = {
        }
        data = {
            "username": PADDLE_ICAFE_USER,
            "password": PADDLE_ICAFE_PASSD,
            "creator" : fields.get("rd_owner"),
            "issues": [icafe_info]
        }
        result = await CreateCard(data).get_data()
        #print("guozhengxin test, result=%s" %result)
        #TODO 异步刷新要支持卡片信息回传
        return result

async def get_cards_by_filter(page=1, page_num=20, iql=None):
    """
    返回指定类型的数据详情
    """
    result = await GetCards({
        'u': PADDLE_ICAFE_USER,
        'pw': PADDLE_ICAFE_PASSD,
        'page': page,
        'maxRecords': page_num,
        'iql': iql
    }).get_data()
    #总共页数
    page_size = result.get('pageSize')
    #当前所在页
    current_page = result.get("currentPage")
    icafeData = result.get('cards', [])
    # 按照前端展示过滤下要展示的字段1
    result = []
    for item in icafeData:
        space = item.get('spacePrefixCode')
        sequence = item.get('sequence')
        level = ""
        rd_owner = ""
        qa_owner = ""
        properties = item.get("properties", [])
        for arr in properties:
            if arr.get("propertyName") == "优先级":
                level = arr.get("displayValue")
            elif arr.get("propertyName") == "QA负责人":
                qa_owner = arr.get("displayValue")
            elif arr.get("propertyName") == "RD负责人":
                rd_owner = arr.get("displayValue")
        tmp = {
            "sequence": item.get('sequence'),
            "title": item.get("title"),
            "status": item.get("status"),
            #TODO 明确用户信息返回邮箱还是中文名称
            "createdUser": item.get("createdUser"),
            "url": baseUrl.format(space=space, sequence=sequence),
            "rd_owner": rd_owner,
            "qa_owner": qa_owner,
            "page_size": page_size,
            "currnet_page": current_page
            #TODO 通过icafeid查询db获取测试中/测试完成的测试服务报告
        }
        result.append(tmp)
    #TODO返回总页数，以及result list
    return len(result), result

class ProjectManage(MABaseView):

    async def get(self, **kwargs):
        """
        调用基类的get方法
        """
        return await super().get(**kwargs)

    async def get_data(self, **kwargs):
        """
        响应请求, 实现获取数据逻辑, 并返回符合查询条件的数据
        """
        query_params = {}
        page = kwargs.get("page", 1)
        pagesize = kwargs.get("pagesize", 20)
        #优先支持RD查询所有卡片，并分页
        #其它字段可以按需支持比如卡片号
        rd = kwargs.get("rd")
        if rd:
            query_params["rd"] = rd
        qa = kwargs.get("qa")
        if qa:
            query_params["qa"] = qa
        #TOTO 使用aio_filter_details_with_total_count获取总数和分页结果	
        count, data = await Project.aio_filter_details_with_total_count(
            page_index=page, limit=pagesize, **query_params, need_all=False
        )
        print("gzx in progject view", "count=", count, "data=", data) 
        return count, data

    async def post(self, **kwargs):
        """
        调用基类的post方法
        """
        return await super().post(**kwargs)

    async def post_data(self, **kwargs):
        """
        响应请求, 实现数据插入
        """
        #TODO icafe已经存在，新建一条，测试id保证不重复
        #还是icafe历史测试id不保留
        count, project_id = await Project.aio_insert(validated_data=kwargs)
        print("project_id=", project_id)
        return {"id" : project_id}

    async def put(self, **kwargs):
        """
        调用基类的put方法
        """
        return await super().put(**kwargs)

    async def put_data(self, **kwargs):
        """
        响应请求，实现数据更新，主要是更新测试任务状态
        """
        test_id = kwargs.get("test_id")
        kwargs.pop("test_id")
        await Project.aio_update(
            validated_data=kwargs, params_data={"test_id": test_id}
        )
        status = kwargs.get("test_status")
        await update_icafe(**kwargs)
 
async def update_icafe(**kwargs):
    #TOTO 梳理卡片required字段更新对应icafe卡片
    #验证，如果缺少required字段,更新卡片状态会失败
    pass
    test_status = kwargs.get("test_status")
    rd = kwargs.get("rd")
    test_id = kwargs.get("test_id")
    icafe_id = kwargs.get("icafe_id")
    status_str_format = "流程状态={}"
    if test_status == 1:
        status_str = status_str_format.fromat("测试中")
    elif test_status == 2:
        #测试未通过不需要修改卡片状态
        status_str = status_str_format.fromat("测试完成")
    else:
        return {}
    if not icafe_id and test_id:
       #TODO查询DB获取所有id
       print("查db获取card_id")
    await ModifyCardStatus({
        'u': PADDLE_ICAFE_USER,
        'pw': PADDLE_ICAFE_PASSD,
        'operator' : rd,
        'fields': [status_str]
    }).get_data(**{"card_id":icafe_id})
 
 
      

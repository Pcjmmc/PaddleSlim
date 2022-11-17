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
        need_status = kwargs.get("status")
        page = kwargs.get("page") if kwargs.get("page") else "1"
        page_num = kwargs.get("page_num") if kwargs.get("page_num") else "20" 
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
        rd = kwargs.get('rd')
        qa = kwargs.get('qa')
        keyword = kwargs.get('keyword')
        iql = ""
        if need_status:
        # 待提测
            #保留Task和bug
            iql = "流程状态 in ({}) AND 类型 in (Task) AND 最后修改时间 > {} AND 最后修改时间 < {}".format(need_status, begin_time, end_time)
        else:
            iql = "类型 in (Task) AND 最后修改时间 > {} AND 最后修改时间 < {}".format(begin_time, end_time)
        if rd:
            sub_iql = " AND (负责人 in ({}) OR RD负责人 in ({}))".format(rd, rd)
            iql = iql + sub_iql
        if qa:
            sub_iql = " AND qa负责人 in ({})".format(qa)
            if qa in ["zhangdeyin", "weike"]:
                sub_iql = ""
            iql = iql + sub_iql
        if keyword:
            sub_iql = " AND 关键字 ~ {}".format(keyword)
            iql = iql + sub_iql
        print("iql=", iql)
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
        type = kwargs.get("type") if kwargs.get("type") else "Task"
        # repo和产品保持一致（这里填充，减少后续卡片状态修改报错）
        repo = kwargs.get("repo") if kwargs.get("repo") else "Paddle"
        icafe_info = {
            "title": kwargs.get("title"),
            #TODO 创建卡片类型是否需要放开，暂时默认为Task
            "type": type,
            "detail": kwargs.get("detail"),
            "creator" : kwargs.get("rd_owner"),
            "fields" : {}
        }
        icafe_info["fields"] = {
            "repo" : repo,
            "负责人" : kwargs.get("rd_owner"),
            "RD负责人": kwargs.get("rd_owner"),
            "QA负责人": kwargs.get("qa_owner")
        }
        data = {
            "username": PADDLE_ICAFE_USER,
            "password": PADDLE_ICAFE_PASSD,
            "creator" : kwargs.get("rd_owner"),
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
        'iql': iql,
    }).get_data()
    total = result.get("total")
    #print(total)
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
        rd_owner = {}
        qa_owner = {}
        properties = item.get("properties", [])
        repo = ""
        pr = ""
        for arr in properties:
            if arr.get("propertyName") == "QA负责人":
                qa_owner["name"] = arr.get("displayValue")
                qa_owner['username'] = arr.get("value")
            elif arr.get("propertyName") == "RD负责人":
                rd_owner["name"] = arr.get("displayValue")
                rd_owner["username"] = arr.get("value")
            elif arr.get("propertyName") == "repo":
                 repo = arr.get("displayValue") if arr.get("displayValue") else ""
            elif arr.get("propertyName") == "PR链接":
                 pr_link = arr.get("value") 
                 if pr_link:
                     pr = pr_link.split("/")[-1]
        #获取提测信息，order by updated time
        query_params = {}
        query_params["icafe_id"] = item.get('sequence')
        test_info_list = await Project().aio_filter_details(need_all=True, order_by="-created", group_by=None, **query_params)
        test_info = {}
        if test_info_list:
            test_info = test_info_list[0]
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
            "repo": repo,
            "pr": pr,
            "currnet_page": current_page,
            "test_id":  test_info.get("test_id") if test_info.get("test_id") else "",
            "test_status" : test_info.get("test_status") if test_info.get("test_status") else "",
            "approve": test_info.get("approve") if test_info.get("approve") else "",
            #TODO 通过icafeid查询db获取测试中/测试完成的测试服务报告
        }
        result.append(tmp)
    #TODO返回总页数，以及result list
    return total, result

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
        #print("gzx in progject view", "count=", count, "data=", data) 
        return count, data

    async def post(self, **kwargs):
        """
        调用基类的post方法
        """
        return await super().post(**kwargs)

    async def post_data(self, **kwargs):
        """
        响应请求, 实现数据插入, 支持测试
        """
        #TODO icafe已经存在，新建一条，测试id保证不重复
        #TODO 重复提测的卡片，需要梳理方案，防止出现多次重复提测
        icafe_id = kwargs.get("icafe_id")
        method = kwargs.get("method") if kwargs.get("method") else "测试"
        if "method" in kwargs.keys():
            kwargs.pop("method")
        if not icafe_id:
           return {}
        if method == "测试":
            count, project_id = await Project.aio_insert(validated_data=kwargs)
            kwargs["method"] = method
            await update_icafe(**kwargs)
            return {"id" : project_id}
        elif method == "提测":
            kwargs["method"] = method
            await update_icafe(**kwargs)

    async def put(self, **kwargs):
        """
        调用基类的put方法
        """
        return await super().put(**kwargs)

    async def put_data(self, **kwargs):
        """
        响应请求，实现数据更新，支持rd提测和qa确认，更新卡片状态
        """
        method = kwargs.get("method") if kwargs.get("method") else "确认"
        #操作卡片需要rd信息，否则会为api user操作
        query_params = {}
        if method == "确认":
            query_params["approve"]  = None
            query_params["icafe_id"] = kwargs.get("icafe_id")
            #明确确认时是否能拿到test_id
            test_id = kwargs.get("test_id")
            if test_id:
                query_params["test_id"] = kwargs.get("test_id")
            else:
                query_params["test_id__ne"] = None
        else:
            return {}
        await Project.aio_update(validated_data=kwargs, params_data=query_params)
        approve = kwargs.get("approve")
        if approve == "pass":
            await update_icafe(**kwargs)

async def update_icafe(**kwargs):
    #TOTO 梳理卡片required字段更新对应icafe卡片
    #验证，如果缺少required字段,更新卡片状态会失败
    rd = kwargs.get("rd")
    qa = kwargs.get("qa")
    test_id = kwargs.get("test_id")
    icafe_id = kwargs.get("icafe_id")
    test_status = kwargs.get("test_status")
    method = kwargs.get("method")
    operator = ""
    target = None
    fields_list = []
    if method == "提测":
        target = "测试中"
        operator = rd
        if rd:
            fields_list.append("RD负责人={}".format(rd))
        if qa:
            fields_list.append("QA负责人={}".format(qa))
    elif method == "测试":
        target = "测试中"
        operator = qa
    elif method == "确认":
        operator = qa
        target = "测试完成"
    else:
        return 
    status_str_format = "流程状态={}"
    if target:
        status_str = status_str_format.format(target)
    else:
        return {}
    fields_list.append(status_str)
    repo = kwargs.get("repo")
    pr = kwargs.get("pr")
    if repo:
        fields_list.append("repo={}".format(repo))
    if pr:
        if repo and  "pull" not in str(pr):
             pr = "github.com/PaddlePaddle/{}/pull/{}".format(repo, pr) 
        fields_list.append("PR链接={}".format(pr))
    if not icafe_id and test_id:
       #TODO查询DB获取所有id
       print("查db获取card_id")
       return 
    await ModifyCardStatus({
        'u': PADDLE_ICAFE_USER,
        'pw': PADDLE_ICAFE_PASSD,
        'isCheckStatus': False,
        'operator' : operator,
        'fields': fields_list
    }).get_data(**{"card_id":icafe_id})
 

#!/bin/env python
# -*- coding: utf-8 -*-
# @author DDDivano
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python

#!/bin/env python
# -*- coding: utf-8 -*-
# @author DDDivano
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python
import asyncio
import json

from views.base_view import MABaseView
from models.api_benchmark import Job, Case
from exception import HTTP400Error
from datetime import datetime
import requests

class GetVersion(MABaseView):
    """
    查看version
    """
    async def get(self, **kwargs):
        return await super().get(**kwargs)

    async def get_data(self, **kwargs):
        cuda = kwargs.get("cuda")
        os = kwargs.get("os")
        data =  await Job.aio_filter_details(need_all=True,cuda=cuda, status="done", mode="schedule", system=os)
        print(data)
        res = []
        for i in data:
            temp = {
                "id": i["id"],
                "framework": i["framework"],
                "commit": i["commit"],
                "create_time": str(i["create_time"]),
                "snapshot": i["snapshot"]
            }
            res.append(temp)
        return len(data), res


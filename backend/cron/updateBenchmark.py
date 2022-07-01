# encoding: utf-8
import asyncio
import os
import shutil
import sys

import aioredis
import wget
import yaml

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from app.ce.benchmark.cache import BenchmarkCase
from ce_web.settings.common import PROJECT_ROOT, path


async def update_benchmark_config(url="https://paddle-qa.bj.bcebos.com/github/nn.yml"):
    # download config
    result = read_remote_yaml(url=url)
    # 更新缓存
    await BenchmarkCase.set_value(result)
    delete_path()


def delete_path():
    out = path(PROJECT_ROOT, "opBenchemarkConf")
    if os.path.exists(out):
        shutil.rmtree(out)

def read_remote_yaml(url):
    _, file_name = url.rsplit("/", 1)
    out = path(PROJECT_ROOT, "opBenchemarkConf")
    if not os.path.exists(out):
        # 不存在则创建路径
        os.makedirs(out)
    whl_file = path(out, file_name)
    # 判断下是否存在改文件存在则删除
    if file_name and os.path.exists(whl_file):
        os.remove(whl_file)
    wget.download(url, out=out)
    try:
        f = open(whl_file, encoding="utf-8")
        store_dict = yaml.load(f, Loader=yaml.FullLoader)
    except Exception as e:
        store_dict = {}
    finally:
        f.close()
    # print(store_dict)
    return store_dict


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(update_benchmark_config())

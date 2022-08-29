# encoding: utf-8
"""
自定义api的参数检验逻辑，比较简单
"""
class AddCaseForm(object):
    """
    实现参数名和类型的检测
    """
    post_data_params = {
        "build_type_id": [str],
        "build_id": [int, str],
        "repo": [str],
        "tag": [str],
        "commit_id": [int, str],
        "commit_time": [int, str],
        "status": [str],
        "test_step": [str, int],
        "job_id": [int, str],
        "build_time": [int, str],
    }
    need_data_params = ["build_type_id", "build_id", "repo", "tag", "commit_id", "test_step", "status"] 

    @classmethod
    def check_request_data(cls, **kwargs):
        """
        参数和类型检测逻辑
        """
        invalid_params = []
        type_error = []
        for key, val in kwargs.items():
            if key not in cls.post_data_params:
                invalid_params.append(key)
            elif type(val) not in cls.post_data_params[key]:
                type_error.append(key)

        if invalid_params or type_error:
            msg = ''
            if invalid_params:
                par_msg = ",".join(invalid_params)
                msg = "无效的参数{} ".format(par_msg)
            if type_error:
                type_msg = ",".join(type_error)
                msg += "类型错误{}".format(type_msg)
            return False, msg
        for need_key in cls.need_data_params:
            if need_key not in kwargs.keys():
                msg ="缺少必要的参数{} ".format(need_key)
                return False, msg
        return True, None

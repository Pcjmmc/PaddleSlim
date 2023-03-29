"""
test
"""
import subprocess

# 定义命令
command = 'python3.9 -c "import paddle; paddle.utils.run_check()"'

# 执行命令并捕获输出
result = subprocess.run(command, shell=True, capture_output=True)

# 打印错误码
print(result.returncode)

# 打印输出结果
print(result.stdout.decode('utf-8'))
print(result.stderr.decode('utf-8'))
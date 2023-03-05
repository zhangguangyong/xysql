### 准备自己的pypi账号

- [注册地址](https://pypi.org/)
- 激活账号
- 配置认证 (~/.pypirc)

```
[pypi]
username = __token__
password = x
```

### 在github创建一个项目

- [github](https://www.github.com)

### 准备环境

- 将项目setup.py下的setup.py复制到自己项目路径下
- [setup.py](https://github.com/navdeep-G/setup.py)
- 修改setup.py填写自己的项目信息
- 安装 twine (pip install twine)
- 生成部署文件 (python setup.py sdist)
- 上传部署文件 (twine upload dist/*)
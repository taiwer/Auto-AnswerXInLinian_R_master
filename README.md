# 新理念全自动答题

Forked from lnnei/Auto-AnswerXinLinian

Several Modifications have been done...
### 什么被提升了

· 支持Part数量任意的测试，适用所有情况

· 支持双项选择题，填空，翻译自动填写（支持所有题型）

· 支持填写完成自动交卷，并开始下一次测试

· 遍历所有页面寻找测试，若无测试则退出

· 控分功能加入

### Todo List

· 测试时间控制

### 他能做什么

- 他可以在10秒钟之内完成答题。

- 是的，他是全自动的。你不需要选择任何东西。

- 100分，Yes！(可以自行控制分数）

- 他能从服务器获取答案，并且用正则表达式很快的解析答案，完成答题。

### 你需要做什么

- 你需要安装Python3以上版本，并且正确安装Requests库，selenium库，Chrome以及对应的WebDriver。

- 你需要在`config.json`中编辑配置

- 运行`main.py`

- 除此之外你不需要做任何事。

### 配置说明

`username,password`: As its name.

`root`: 改成学校平台对应的地址

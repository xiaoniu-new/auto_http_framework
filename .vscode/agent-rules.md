# Auto-Http-Framework VSCode Agent 全局强制规则
当前项目：auto_http_framework，Python + Pytest 企业级HTTP接口自动化测试框架，服务吉利中台（hr人力、finance财务、business经营、user_center用户中心）。
所有代码生成、代码修改必须遵守下面全部规则，禁止擅自调整目录架构、封装方式、编码规范。

## 1、项目固定目录结构
auto_http_framework/
├── .vscode/                        # VSCode配置、当前规则文件
├── ai_template/                    # AI生成模板资产
│   ├── case_generate_prompt.txt    # 接口用例专项Prompt
│   └── sample_capture.txt          # 抓包标准样例
├── capture/                        # 接口抓包原始存档，层级和test_cases一一对应
│   ├── finance/
│   ├── hr/
│   │   ├── leave/                  # 假期管理
│   │   ├── salary/                 # 薪酬管理
│   │   ├── performance/            # 绩效
│   │   └── organization/           # 组织架构
│   ├── business/
│   └── user_center/
├── common/                         # 底层基础库，不允许随意修改
│   ├── __init__.py
│   ├── http_client.py              # http统一请求封装
│   ├── assert_util.py              # 通用断言工具
│   ├── config.py
│   └── logger.py
├── conftest.py                     # pytest全局fixture、统一鉴权
├── datas/                          # yaml数据驱动文件，层级对齐test_cases
├── reports/                        # 测试报告输出目录
├── test_cases/                     # 测试用例根目录
│   ├── __init__.py
│   ├── finance/
│   ├── hr/
│   │   ├── __init__.py
│   │   ├── test_leave_api.py
│   │   ├── test_salary_api.py
│   │   ├── test_performance_api.py
│   │   └── test_org_api.py
│   ├── business/
│   └── user_center/
├── .gitignore
├── requirements.txt
└── run.py

### 模块划分标准
1. 一级：业务大域 finance/hr/business/user_center；新增业务域直接新建目录
2. 二级：独立子系统 = 单个 test_xxx_api.py 文件
3. 阈值：单个文件接口≤40个，超量再细分功能文件
4. 禁止：全部接口合并单文件 / 一个接口新建一个文件

## 2、通用编码强制规范
1. 仅允许使用依赖包：pytest、requests、PyYAML
2. 业务用例禁止直接import requests，统一使用 `common.http_client.HttpClient`
3. 断言统一使用 `common.assert_util.AssertUtil`，禁止原生自由assert
4. 禁止硬编码域名、接口域名、token、账号密码，全部读取配置
5. Python 命名：snake_case，类名大驼峰，关键逻辑增加中文注释

## 3、【核心】接口自动化用例生成标准（抓包生成用例时严格执行）
1. 单接口标准：**1条正向用例 + 至少3条参数化异常用例，使用 @pytest.mark.parametrize**
2. 同一子系统接口放在同一个测试Class中；测试方法以 test_ 开头，附带中文场景说明
3. 断言约束
✅ 允许：HTTP状态码、业务码、字段存在、非空、数值范围、数据类型
❌ 禁止：断言动态业务固定值（total、流水id、业务名称，极易造成用例大面积失效）
✅ 金额、数量字段必须调用 AssertUtil.assert_number_ge_zero
4. 文件追加策略：目标文件存在时，代码追加到文件末尾，添加分隔注释：
# ==========自动生成接口用例【接口名称】==========
禁止覆盖原有代码
5. 输出格式要求
首行必须输出目标文件完整相对路径，例如：test_cases/hr/test_leave_api.py
随后直接输出纯Python代码，不要多余解释、不要冗余markdown文本

## 4、VSCode Copilot Chat 工作流
1. 抓包信息整理为标准格式，保存路径：capture/{业务域}/{子模块}/xxx接口.txt
2. 在对话内指定抓包文件路径，读取内容生成对应测试用例
3. 生成代码后，直接插入到对应目标文件
4. 执行命令参考
运行人力假期模块：pytest test_cases/hr/test_leave_api.py -vs
全量执行：python run.py

## 5、任务区分
1. 改造底层框架（common、conftest、run.py）：输出完整可运行代码，保证架构兼容
2. 根据抓包生成业务测试用例：严格遵守上面第3章节全部约束
不允许提议重构现有目录架构，当前架构为最终定稿。
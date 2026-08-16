# Auto Http Framework

这是一个基于 Python + Pytest 的企业级 HTTP 接口自动化测试框架，适用于中后台的 hr、finance、business、user_center 等业务域。

## 目录架构

- `ai_template/`: AI 生成模板与抓包样例
- `capture/`: 抓包原始存档，按业务域和模块组织
- `common/`: 公共 HTTP、断言、配置、日志基础库
- `datas/`: YAML 数据驱动文件
- `test_cases/`: 测试用例目录，按业务域和子模块组织
- `reports/`: 测试报告输出目录

## 快速开始

1. 安装依赖：
   ```bash
   按照"安装python虚拟环境"在项目下安装虚拟环境
   ```
2. 配置环境变量或在 `datas/config/` 下为每个业务域添加对应的 YAML（遵循多业务域独立配置约束）：
   - 公共配置：`datas/config/common.yaml`
   - 域配置示例：`datas/config/hr.yaml`、`datas/config/finance.yaml`、`datas/config/business.yaml`、`datas/config/user_center.yaml`
   示例环境变量方式（可选，用于快速覆盖）：
   ```bash
   export ENABLE_LIVE_API=false
   export PRODUCT_LINE=hr    # 或者在 pytest 中使用 --product-line=hr
   ```
3. 运行全部用例：
   ```bash
   1）执行 source venv/bin/activate 先激活虚拟环境
   2）执行 python3 run.py
   ```
4. 运行单个模块：
   ```bash
   pytest test_cases/hr/test_leave_api.py -vs
   ```

## 代码规范

- 禁止直接使用 `requests`；统一使用 `common.http_client.HttpClient`
- 禁止原生 `assert`；统一使用 `common.assert_util.AssertUtil`
- 禁止硬编码域名、接口地址、token、账号密码
- 业务用例采用 `pytest.mark.parametrize` 设计异常参数化验证

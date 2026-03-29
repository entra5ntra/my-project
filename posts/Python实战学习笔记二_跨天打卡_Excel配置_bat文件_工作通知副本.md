# Python实战学习笔记（二）

## 一、跨天打卡的数据归属问题

### 问题
员工8:57上班，凌晨00:23下班。API返回的时间戳带完整日期，00:23的记录日期是第二天。
如果按日期分组，00:23被归到第二天，导致：
- 当天只有上班卡 → 变成"缺卡"
- 第二天多了一条凌晨记录 → 工时被污染（00:23到当天下班，算出20多小时）

### 解决方案
凌晨0:00~5:59的打卡自动归到前一天：
```python
from datetime import datetime, timedelta

dt = ts_to_dt(check_time)
if dt.hour < 6:
    # 凌晨打卡归前一天
    date_str = (dt - timedelta(days=1)).strftime("%Y-%m-%d")
else:
    date_str = dt.strftime("%Y-%m-%d")
```

### 为什么是6点？
正常没有人凌晨6点前上班，这个时间段的打卡一定是前一天的下班卡。

---

## 二、从配置文件到Excel配置表的演进

### 阶段1：硬编码在代码里
```python
# 最差的做法：改规则就要改代码
if name == "陈雪兰":
    start = actual_time
```

### 阶段2：JSON配置文件（config.json）
```json
{
    "陈雪兰": {"start_rule": "actual", "lunch_deduct": false}
}
```
好处：改规则不用改代码。
问题：考勤文员不会编辑JSON（格式严格，多个逗号就报错）。

### 阶段3：Excel配置表
```
姓名     | 上班规则 | 扣午饭 | 扣晚饭 | 标准工时
陈雪兰   | 实际     | 否     | 否     | 8
吴凤娟   | 9:00     | 否     | 是     | 8
```
好处：文员会用Excel，改完保存就行，不需要懂代码。

### 代码怎么读Excel配置
```python
import openpyxl

def load_employee_rules():
    rules = {}
    wb = openpyxl.load_workbook("员工规则表.xlsx")
    ws = wb.active
    for r in range(2, ws.max_row + 1):
        name = ws.cell(r, 1).value
        if not name:
            continue
        start_rule = str(ws.cell(r, 2).value or "9:00").strip()
        lunch = str(ws.cell(r, 3).value or "是").strip()

        rules[name] = {
            "start_rule": "actual" if "实际" in start_rule else "9:00",
            "lunch_deduct": lunch != "否",
        }
    return rules
```

### 配置优先级设计
```
Excel规则表 > config.json里的个人配置 > config.json里的_default默认值
```
这样文员改Excel就能覆盖所有设置，你也可以在config.json里做底层配置。

---

## 三、bat文件（批处理）

### 什么是bat文件
Windows的批处理脚本，双击就能执行一系列命令。扩展名必须是`.bat`，不是`.bat.txt`。

### 基本语法
```bat
@echo off                  :: 不显示命令本身
chcp 65001 >nul           :: 设置中文编码（UTF-8）
title 我的程序             :: 窗口标题
cd /d "%~dp0"              :: 切换到bat文件所在目录（关键！）
python main.py monthly     :: 执行Python脚本
pause                      :: 等待用户按键再关闭窗口
```

### 关键命令解释

`@echo off` — 不在窗口里显示每行命令，只显示输出结果

`chcp 65001 >nul` — 切换到UTF-8编码，否则中文会乱码。`>nul`表示不显示切换提示

`cd /d "%~dp0"` — 这个很重要：
- `%~dp0` = bat文件自己所在的目录路径
- `cd /d` = 切换到那个目录（包括切换盘符）
- 没有这行的话，Python可能找不到同目录的config.json

`pause` — 程序跑完后窗口不会立刻关闭，等你按任意键

### 定时运行bat（Windows任务计划）
1. 开始菜单搜索"任务计划程序"
2. 右侧点"创建基本任务"
3. 触发器选"每天"，设置时间（如9:30）
4. 操作选"启动程序"，浏览选你的bat文件
5. 完成

---

## 四、钉钉工作通知（私聊消息）

### 和群机器人的区别

| | 群机器人 | 工作通知 |
|--|---------|---------|
| 发到哪 | 群聊 | 个人私聊 |
| 谁能看 | 群里所有人 | 只有指定的人 |
| 需要什么 | webhook地址 | agent_id + userid |
| 适合场景 | 群公告 | 通知特定人 |

### API接口
```
POST https://oapi.dingtalk.com/topapi/message/corpconversation/asyncsend_v2
参数:
  - agent_id: 应用的AgentID（开发者后台查看）
  - userid_list: 接收人的userid（逗号分隔）
  - msg: 消息内容（JSON格式）
```

### 代码实现
```python
def send_work_notice(self, agent_id, userid_list, text):
    body = {
        "agent_id": agent_id,
        "userid_list": userid_list,
        "msg": {
            "msgtype": "text",
            "text": {"content": text}
        }
    }
    r = requests.post(
        f"{self.BASE}/topapi/message/corpconversation/asyncsend_v2",
        params={"access_token": self.token},
        json=body
    )
    return r.json()
```

### agent_id在哪找
钉钉开发者后台 → 你的应用 → 应用详情页 → 基础信息里有AgentId

---

## 五、程序的交互设计：让非技术人员能用

### 命令行参数 vs 交互式菜单

**命令行参数**（给你自己用）：
```
python main.py monthly 2026-02
```

**交互式菜单**（给文员用）：
```python
def main():
    if len(sys.argv) < 2:
        # 没有参数 = 双击bat运行，显示菜单
        print("1. 生成月度工时表")
        print("2. 异常打卡检查")
        choice = input("请选择: ")
        if choice == "1":
            ym = input("请输入月份(如 2026-02): ")
            monthly_report(ym)
    else:
        # 有参数 = 命令行调用
        cmd = sys.argv[1]
        ...
```

这样同一个程序：
- 双击bat运行 → 弹菜单让文员选
- 命令行带参数运行 → 直接执行（定时任务用）

### 防崩溃设计
```python
# bat运行时，报错了窗口不能直接关掉，要让用户看到错误信息
try:
    config = load_config()
except Exception as e:
    print(f"出错了: {e}")
    input("按回车退出...")  # 窗口停住，不会一闪而过
    sys.exit(1)
```

---

## 六、数据验证的方法论

### 这次验证工时表的完整流程

1. **先和钉钉原始数据对比**（100%匹配才说明API拉取正确）
   - 钉钉导出的打卡记录 vs 程序拉取的打卡记录
   - 发现bug：每7天分段的最后一天数据丢失

2. **再和手工计算对比**（发现规则差异）
   - 程序生成的工时 vs 考勤文员手工算的工时
   - 发现：晚饭界线不是18:30而是19:00
   - 发现：部分员工是连班不扣午饭

3. **分类分析差异**
   - 差-30分 → 扣饭规则不同
   - 差+30分 → 连班手动调整
   - 差-60/-90 → 特殊员工人为改动

4. **逐步修正规则，缩小差异**
   - 晚饭18:30 → 19:00
   - 加入个人配置（连班、推单文员）
   - 最终可自动计算的部分达到95%以上

### 核心思路
不要想着一次做对，而是：写代码 → 跑数据 → 对比 → 找差异规律 → 修正 → 再对比。
每轮对比都缩小差异范围，直到剩下的都是必须人工处理的特殊情况。

---

## 七、文件路径处理

### Path对象（推荐）
```python
from pathlib import Path

# 获取当前脚本所在目录
BASE_DIR = Path(__file__).parent

# 拼接路径
config_path = BASE_DIR / "config.json"
rules_path = BASE_DIR / "员工规则表.xlsx"
output_dir = BASE_DIR / "output"

# 创建目录（不存在才创建）
output_dir.mkdir(exist_ok=True)

# 判断文件是否存在
if rules_path.exists():
    print("规则表存在")

# 获取绝对路径
print(config_path.resolve())
```

### 为什么bat里要 cd /d "%~dp0"
双击bat时，当前工作目录可能不是bat所在目录（比如可能是桌面或系统目录）。
`cd /d "%~dp0"` 确保切换到bat所在目录，这样Python里的相对路径才能正确找到config.json。

Python里用 `Path(__file__).parent` 也是同样的道理——确保不管从哪里运行脚本，都能找到同目录的文件。

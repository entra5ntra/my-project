# Python实战学习笔记

## 一、钉钉API打卡数据拉取的教训

### 1. checkDateTo 时间截断问题（最大的坑）

**问题：** 程序按7天分段拉取打卡数据，每段最后一天的数据全部丢失。
2月份分4段拉取，2/7、2/14、2/21、2/28四天的打卡全部显示为"休"。

**原因：** 钉钉API的 `checkDateTo` 参数是精确截断的。
官方文档原话：参数传 `"2021-12-01 18:00:00"`，员工在 `19:00` 的打卡信息获取不到。

**错误代码：**
```python
# chunk_end 算出来是 2026-02-07 00:00:00
# 这意味着2月7号00:00之后的所有打卡都拿不到！
cur = start  # 2026-02-01 00:00:00
chunk_end = cur + timedelta(days=6)  # 2026-02-07 00:00:00
df = cur.strftime("%Y-%m-%d %H:%M:%S")   # "2026-02-01 00:00:00"
dt = chunk_end.strftime("%Y-%m-%d %H:%M:%S")  # "2026-02-07 00:00:00" ← 问题在这
```

**正确代码：**
```python
# 直接用日期数字拼接，确保每段结束时间是 23:59:59
day_start = 1
while day_start <= days:
    day_end = min(day_start + 6, days)
    df = f"{year}-{month:02d}-{day_start:02d} 00:00:00"
    dt = f"{year}-{month:02d}-{day_end:02d} 23:59:59"  # ← 明确写死23:59:59
    records = api.get_attendance_records(user_ids, df, dt)
    day_start = day_end + 1
```

**教训：** 用 `datetime` 加减运算时，时分秒会跟着变化。
如果只关心"日期"级别的范围，最安全的做法是用整数日期拼接字符串，不要依赖 `timedelta` 的时间部分。

---

### 2. 毫秒时间戳 vs 字符串时间

**问题：** 钉钉API返回的 `userCheckTime` 是毫秒级时间戳（如 `1599450909000`），不是可读的时间字符串。

**正确处理：**
```python
from datetime import datetime

def ts_to_dt(ms_timestamp):
    """毫秒时间戳转datetime"""
    return datetime.fromtimestamp(int(ms_timestamp) / 1000)
    #                                                ^^^^^ 除以1000！

# 示例
ts = 1599450909000
dt = ts_to_dt(ts)  # 2020-09-07 10:15:09
```

**常见错误：** 忘记除以1000，得到一个遥远未来的日期。

---

### 3. API分页和批量限制

钉钉考勤API有两个硬限制：
- **时间跨度：最多7天**
- **人数：最多50人/次**

必须自己做分段和分批：
```python
# 按50人一组分批
for i in range(0, len(user_ids), 50):
    batch = user_ids[i:i+50]
    records = api.get_records(batch, date_from, date_to)
```

**教训：** 调用第三方API前，一定要先看清楚文档里的限制条件。
不要假设"一次全拉"能行。

---

### 4. API限流保护

**问题：** 连续快速调用钉钉接口，会被限流封禁。

**解决：** 每次API调用后加一个短暂延时：
```python
import time

for batch in batches:
    result = api.call(batch)
    time.sleep(0.5)  # 等半秒再发下一个请求
```

---

### 5. 未来日期和当天日期的处理

**问题：** 生成月度报表时，未来日期显示"休"，当天显示"缺卡"。

**逻辑应该是：**
- 已过去的日期无打卡 → 显示"休"（确实没上班）
- 今天 → 留空（还没下班，不能判断）
- 未来日期 → 留空（还没到）

```python
from datetime import datetime

today = datetime.now().date()
this_date = datetime(year, month, day).date()

if this_date >= today:
    # 今天和未来：留空
    pass
elif has_clock_data:
    # 过去有打卡：计算工时
    calc_work()
else:
    # 过去无打卡：休息
    show_rest()
```

**教训：** 报表程序不只是计算数据，还要考虑"时间维度"的边界。

---

### 6. JSON配置文件格式错误

**问题：** 手动编辑 `config.json` 时多打了一个字符 `p`，导致程序报错：
```
json.decoder.JSONDecodeError: Expecting ',' delimiter: line 13 column 10
```

**教训：** JSON格式非常严格——多一个字符、少一个逗号都会报错。
建议编辑后用在线JSON校验工具检查一下，或者在代码里加错误提示：
```python
try:
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
except json.JSONDecodeError as e:
    print(f"config.json格式错误: {e}")
    print("请检查JSON格式是否正确（逗号、引号、大括号等）")
    sys.exit(1)
```

---

## 二、try/except 异常处理

### 1. 基本语法

```python
try:
    # 可能出错的代码
    result = 10 / 0
except ZeroDivisionError:
    # 处理特定错误
    print("不能除以零")
except Exception as e:
    # 处理所有其他错误
    print(f"出错了: {e}")
finally:
    # 无论是否出错都会执行（可选）
    print("清理工作")
```

### 2. 常见的异常类型

| 异常类型 | 什么时候出现 | 例子 |
|---------|------------|------|
| FileNotFoundError | 文件不存在 | open('不存在.txt') |
| json.JSONDecodeError | JSON格式错误 | json.loads('{错误}') |
| KeyError | 字典里没有这个key | d['不存在的key'] |
| IndexError | 列表下标越界 | lst[100] |
| TypeError | 类型不匹配 | '文字' + 123 |
| ValueError | 值不对 | int('不是数字') |
| requests.ConnectionError | 网络连接失败 | requests.get(url) |
| requests.Timeout | 请求超时 | requests.get(url, timeout=5) |
| ZeroDivisionError | 除以零 | 10 / 0 |

### 3. 实际应用场景

**场景1：读取配置文件**
```python
def load_config():
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("找不到config.json，请确认文件在同一目录下")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"config.json格式错误第{e.lineno}行: {e.msg}")
        sys.exit(1)
```

**场景2：调用API**
```python
def call_api(url, params):
    try:
        r = requests.get(url, params=params, timeout=30)
        data = r.json()
        if data.get('errcode') != 0:
            print(f"API返回错误: {data.get('errmsg')}")
            return None
        return data
    except requests.ConnectionError:
        print("网络连接失败，请检查网络")
        return None
    except requests.Timeout:
        print("请求超时，稍后重试")
        return None
    except Exception as e:
        print(f"未知错误: {e}")
        return None
```

**场景3：解析数据**
```python
def parse_time(value):
    """安全解析时间，出错返回None而不是崩溃"""
    try:
        return datetime.fromtimestamp(int(value) / 1000)
    except (ValueError, TypeError, OSError):
        print(f"时间解析失败: {value}")
        return None
```

**场景4：批量处理，单条出错不影响整体**
```python
results = []
for item in data_list:
    try:
        result = process(item)
        results.append(result)
    except Exception as e:
        print(f"处理 {item} 出错: {e}，跳过继续")
        # 不return不exit，继续处理下一条
        continue
```

### 4. 什么时候用 try/except

**该用的场景：**
- 读写文件（文件可能不存在或没权限）
- 网络请求（网络可能断、超时、服务器报错）
- 解析外部数据（JSON/Excel/API返回值格式可能不对）
- 用户输入（用户可能输入不合法的值）

**不该用的场景：**
```python
# 错误示范：用try/except代替正常的判断逻辑
try:
    value = my_dict[key]
except KeyError:
    value = default

# 正确做法：用 .get() 方法
value = my_dict.get(key, default)
```

### 5. 黄金法则

1. **只捕获你能处理的异常** — 不要写空的 `except: pass`，这会吞掉所有错误导致调试困难
2. **异常类型写具体** — `except ValueError` 比 `except Exception` 好
3. **给用户有用的错误信息** — 告诉用户出了什么问题、怎么解决
4. **该崩就崩** — 如果配置文件都读不了，程序不应该带着错误继续跑

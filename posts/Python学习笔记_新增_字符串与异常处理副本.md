# Python 学习笔记（新增） — 字符串处理、异常处理、答疑

> 学习日期：2026年3月7日

---

## 一、字符串处理 — SKU清洗必备

### strip() 去两端空格

```python
"  IP16PM - CLEAR  ".strip()    # → "IP16PM - CLEAR"
# 只去两头的空格，中间的不管
```

### replace(旧, 新) 替换内容

```python
# 删空格：把空格替换成空字符串
"IP16PM - CLEAR".replace(" ", "")     # → "IP16PM-CLEAR"

# 换符号：横杠换下划线
"IP16PM-CLEAR".replace("-", "_")      # → "IP16PM_CLEAR"

# 换文字
"透明壳".replace("透明", "磨砂")        # → "磨砂壳"

# 找不到要替换的？不报错，原样返回
"hello".replace("xyz", "abc")          # → "hello"
```

**replace第二个参数给空字符串 `""` 就是删除。**

### split() 按符号切开变列表

```python
"IP16PM-CLEAR-透明壳".split("-")
# → ["IP16PM", "CLEAR", "透明壳"]

# 取切开后的某一段
parts = "IP16PM-CLEAR-透明壳".split("-")
parts[0]    # → "IP16PM"
parts[1]    # → "CLEAR"
parts[2]    # → "透明壳"
```

### upper() / lower() 大小写转换

```python
"ip16pm-clear".upper()     # → "IP16PM-CLEAR"
"IP16PM-CLEAR".lower()     # → "ip16pm-clear"
```

### in 判断是否包含

```python
"CLEAR" in "IP16PM-CLEAR"   # → True
"MATTE" in "IP16PM-CLEAR"   # → False
```

### f-string 格式化拼接

```python
model = "IP16PM"
color = "CLEAR"
f"{model}_{color}"           # → "IP16PM_CLEAR"
```

### 链式调用 — 一个接一个串着写

```python
"  IP16PM - CLEAR ".strip().replace(" ", "").upper()
# 第一步 strip()     → "IP16PM - CLEAR"
# 第二步 replace()   → "IP16PM-CLEAR"
# 第三步 upper()     → "IP16PM-CLEAR"

# 每一步结果都是字符串，所以后面可以继续接 .方法()
```

### 实战：批量清洗SKU数据

```python
raw_list = [
    "  IP16PM - CLEAR ",
    "ip15-ring  ",
    " IP16PM-MATTE",
    "  ip15 - leather  "
]

# 普通写法
result = []
for i in raw_list:
    result.append(i.strip().replace(" ", "").upper())

# 列表推导式写法（语法糖，效果一样）
result = [i.strip().replace(" ", "").upper() for i in raw_list]

# 结果 → ["IP16PM-CLEAR", "IP15-RING", "IP16PM-MATTE", "IP15-LEATHER"]
```

---

## 二、异常处理 try/except — 让程序出错不崩溃

### 基本结构

```python
try:
    # 可能出错的代码
except 错误类型:
    # 出错了怎么办
```

### 常见错误类型

```python
# ValueError — 值的类型不对
try:
    num = int("abc")
except ValueError:
    print("转换失败，不是数字")
    num = 0

# FileNotFoundError — 文件不存在
try:
    with open("不存在.json", "r", encoding="utf-8") as f:
        data = json.load(f)
except FileNotFoundError:
    print("文件不存在")
    data = {}

# KeyError — 字典的key不存在
try:
    price = sku_config["IP99-XXX"]["价格"]
except KeyError:
    print("SKU不存在")
    price = 0

# json.JSONDecodeError — JSON格式有问题
try:
    data = json.load(f)
except json.JSONDecodeError:
    print("JSON格式有问题")
    data = {}

# Exception — 兜底，什么错都接住
try:
    result = 10 / 0
except Exception as e:
    print(f"出错了：{e}")
```

### 多个except — 分别处理不同错误

```python
try:
    # 可能出错的代码
except FileNotFoundError:
    # 文件不存在时
except json.JSONDecodeError:
    # JSON格式坏了时
```

### finally — 不管出不出错都执行

```python
try:
    data = json.load(f)
except Exception as e:
    print(f"读取失败：{e}")
finally:
    print("处理完毕")   # 成功失败都会执行
```

### 实战：安全读取JSON配置文件

```python
import json

def safe_load_config(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        print("文件不存在")
        return {}
    except json.JSONDecodeError:
        print("JSON格式有问题")
        return {}

# 使用：不管出什么错都不崩，都能拿到一个字典
config = safe_load_config("config.json")
```

---

## 三、答疑汇总

### encoding="utf-8" 是什么？

告诉Python用UTF-8编码读写文件。UTF-8能处理中文、英文等所有字符。

```python
# Windows中文系统默认GBK，读UTF-8文件可能乱码
with open("file.json", "r") as f:                       # 可能乱码
with open("file.json", "r", encoding="utf-8") as f:     # 不会乱码
```

**规则：凡是打开文件，都加 `encoding="utf-8"`。**

### 列表 [] 怎么表示？

```python
# 方括号，逗号隔开
fruits = ["苹果", "香蕉", "橘子"]
fruits[0]          # → "苹果"（从0开始数）
fruits.append("西瓜")  # 往末尾加一个
len(fruits)        # → 4（长度）
```

### result = [] 是什么意思？

就是准备一个空箱子，后面用 `.append()` 往里塞东西：

```python
result = []                    # 空箱子
result.append("IP16PM-CLEAR")  # 塞一个
result.append("IP15-RING")     # 再塞一个
# result → ["IP16PM-CLEAR", "IP15-RING"]
```

### 列表推导式是什么？

语法糖，把"创建空列表→循环→append"压成一行：

```python
# 普通写法（4行）
result = []
for x in raw_list:
    result.append(x.strip())

# 列表推导式（1行，效果一样）
result = [x.strip() for x in raw_list]
```

**公式：`[对每个元素做什么 for 元素 in 列表]`**

加筛选条件：`[元素 for 元素 in 列表 if 条件]`

### return 怎么用？

把结果丢回给调用的人，同时函数结束：

```python
# 没有return → 调用方拿到None
def add(a, b):
    result = a + b

x = add(1, 2)    # → None

# 有return → 调用方拿到结果
def add(a, b):
    return a + b

x = add(1, 2)    # → 3
```

**在异常处理里：成功return真数据，失败return兜底值。**

### 链式调用是什么？

不是函数嵌套，是方法一个接一个串着写。每一步结果是字符串，后面就能继续接 `.方法()`：

```python
# 串起来
s = "  IP16PM - CLEAR ".strip().replace(" ", "").upper()

# 等价于拆开写
s = "  IP16PM - CLEAR "
s = s.strip()
s = s.replace(" ", "")
s = s.upper()
```

# Python 常用标准库学习笔记
### os、datetime、json

---

## 1. os 模块

`os` 专门用来**操作文件和文件夹**。

使用前先导入：
```python
import os
```

---

### 常用功能

**获取当前路径**
```python
print(os.getcwd())  # 打印当前工作目录
```

**创建文件夹**
```python
os.mkdir("myfolder")    # 创建单个文件夹
os.makedirs("a/b/c")    # 创建多层文件夹
```

**查看文件夹里有什么**
```python
files = os.listdir(".")  # 列出当前目录所有文件
print(files)
```

**判断文件或文件夹是否存在**
```python
os.path.exists("myfolder")  # 存在返回True，不存在返回False
os.path.isfile("test.txt")  # 判断是不是文件
os.path.isdir("myfolder")   # 判断是不是文件夹
```

**删除文件和文件夹**
```python
os.remove("test.txt")   # 删除文件
os.rmdir("myfolder")    # 删除空文件夹
```

---

### 关于 `os.path` 的点来点去

看到 `.` 就理解成**"里面的"**：

```python
os             # os模块
os.path        # os模块里的"路径部门"
os.path.exists()  # 路径部门里的exists函数
```

就像 OOP 里对象调用方法一样：
```python
dog.bark()         # dog对象的bark方法
os.path.exists()   # os模块的path子模块的exists函数
```

---

### 练习题参考答案

```python
import os

# 1. 打印当前工作目录
print(os.getcwd())

# 2. 创建文件夹
os.mkdir("myproject")

# 3. 判断是否存在
if os.path.exists("myproject"):
    print("文件夹创建成功！")

# 4. 列出当前目录所有文件
files = os.listdir(".")
print(files)
```

---

### 重要提示
- 不需要死记硬背，用到的时候查就行
- 只需要记住 `os` 能做什么，需要的时候知道去哪找

---

## 2. datetime 模块

`datetime` 专门用来处理**日期和时间**。

使用前先导入：
```python
from datetime import datetime
```

---

### 常用功能

**获取当前时间**
```python
now = datetime.now()
print(now)  # 2026-03-15 21:42:30
```

**获取年月日时分秒**
```python
now = datetime.now()
print(now.year)    # 2026
print(now.month)   # 3
print(now.day)     # 15
print(now.hour)    # 21
print(now.minute)  # 42
```

**格式化时间显示**
```python
now = datetime.now()
print(now.strftime("%Y年%m月%d日 %H:%M:%S"))  # 2026年03月15日 21:42:30
```

**计算日期差**
```python
birthday = datetime(2000, 1, 1)
now = datetime.now()
diff = now - birthday
print(diff.days)  # 距离2000年1月1日过了多少天
```

---

### 常用格式符

| 符号 | 含义 |
|------|------|
| `%Y` | 四位年份 |
| `%m` | 月份 |
| `%d` | 日期 |
| `%H` | 小时 |
| `%M` | 分钟 |
| `%S` | 秒 |

---

### `strftime` 是什么？

`strftime` 是 `datetime` 对象自带的方法，就像 OOP 里对象调用方法：

```python
now = datetime.now()  # now是一个datetime对象
now.strftime(...)     # 调用这个对象的strftime方法
```

`strftime` = **string format time**，把时间格式化成字符串

---

### 练习题参考答案

```python
from datetime import datetime

now = datetime.now()

# 1. 格式化打印当前时间
print(now.strftime("现在是：%Y年%m月%d日 %H:%M:%S"))

# 2. 计算活了多少天
birthday = datetime(2001, 1, 1)
diff = now - birthday
print(f"我已经活了{diff.days}天")
```

---

## 3. json 模块

`json` 用来处理 **JSON 数据**，JSON 和 Python 字典长得很像。

使用前先导入：
```python
import json
```

---

### JSON 长什么样？

```json
{
    "name": "小明",
    "age": 18,
    "hobbies": ["篮球", "编程"]
}
```

---

### 四个核心函数

| 函数 | 作用 |
|------|------|
| `json.dumps()` | 字典 → 字符串 |
| `json.loads()` | 字符串 → 字典 |
| `json.dump()` | 字典 → JSON文件 |
| `json.load()` | JSON文件 → 字典 |

**记忆技巧：** 有 `s` 的处理字符串，没有 `s` 的处理文件 😊

---

### 常用功能

**字典 → JSON字符串**
```python
data = {"name": "小明", "age": 18}
json_str = json.dumps(data, ensure_ascii=False)
print(json_str)  # {"name": "小明", "age": 18}
```

**JSON字符串 → 字典**
```python
json_str = '{"name": "小明", "age": 18}'
data = json.loads(json_str)
print(data["name"])  # 小明
```

**写入JSON文件**
```python
data = {"name": "小明", "age": 18}
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
```

**读取JSON文件**
```python
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)
print(data["name"])  # 小明
```

---

## 标准库总结

| 模块 | 作用 | 导入方式 |
|------|------|---------|
| `os` | 操作文件和文件夹 | `import os` |
| `datetime` | 处理日期和时间 | `from datetime import datetime` |
| `json` | 处理JSON数据 | `import json` |

---

*json 练习题待完成：创建个人信息字典，写入json文件，再读取打印*

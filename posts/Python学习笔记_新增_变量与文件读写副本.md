# Python 学习笔记（新增） — 全局/局部变量、文件读写、JSON

> 学习日期：2026年3月6日

---

## 一、全局变量 vs 局部变量

```python
name = "十二辰"          # 全局变量：函数外面，哪都能用

def show_company():
    city = "东莞"         # 局部变量：函数里面，出了函数就没了
    print(f"{name}在{city}")

show_company()            # → 十二辰在东莞
print(name)               # → ✅ 全局变量，外面能用
print(city)               # → ❌ 报错！局部变量，外面用不了
```

**规则：函数里面能看到外面的，外面看不到里面的。**

### 想改全局变量？别用 global，用传参+return

```python
# ❌ 不推荐
def add_one():
    global count
    count = count + 1

# ✅ 推荐：干净清楚
def add_one(n):
    return n + 1

count = 10
count = add_one(count)    # → 11
```

---

## 二、文件读写

### txt 文件

```python
# 写入（"w"覆盖，"a"追加）
with open("log.txt", "w", encoding="utf-8") as f:
    f.write("第一行\n")
    f.write("第二行\n")

# 读取
with open("log.txt", "r", encoding="utf-8") as f:
    content = f.read()       # 整个读完

# 逐行读取
with open("log.txt", "r", encoding="utf-8") as f:
    for line in f:
        print(line.strip())  # strip()去掉末尾换行符
```

**with 的作用：自动关文件，不用手动 f.close()**

三个模式：`"w"` 写（覆盖）、`"a"` 追加、`"r"` 读

---

## 三、JSON 读写 — 最常用

### JSON 是什么？

就是**保存在硬盘上的字典**。程序关了还在，下次打开还能用。

```json
{
  "公司": "十二辰",
  "城市": "东莞",
  "仓库": ["东莞仓", "越南仓", "菲律宾仓"]
}
```

跟 Python 字典几乎一样，唯一区别：JSON 只能用双引号。

### 两个核心函数

```python
import json

# 读：文件 → 字典
with open("config.json", "r", encoding="utf-8") as f:
    data = json.load(f)     # data 就是普通字典，直接用

# 写：字典 → 文件
with open("config.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    # ensure_ascii=False → 中文不乱码
    # indent=2 → 格式化好看
```

| 操作 | 函数 | 方向 |
|------|------|------|
| 读 | `json.load(f)` | 文件 → 字典 |
| 写 | `json.dump(data, f)` | 字典 → 文件 |

### 读出来就是字典，之前学的全能用

```python
data = json.load(f)
data["key"]                          # 普通取值
data.get("key", "兜底值")            # 安全取值
data.get("key", {}).get("子key", 0)  # 嵌套安全取值
for k, v in data.items():            # 遍历
```

---

## 四、实战模板：读取→处理→写回

这是日常写工具的核心套路（考勤工具、发货系统都是这个流程）：

```python
import json

# 1. 读取
with open("sku_config.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 2. 处理（遍历、筛选、修改）
for code, info in data.items():
    print(f"{info['品名']} 售价 {info['价格']}元")

out_of_stock = [code for code, info in data.items() if info["库存"] == 0]

data["IP15-RING"]["库存"] = 0

# 3. 写回
with open("sku_config.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```

# Python 学习笔记 — 字典、函数、列表推导式

> 学习日期：2026年3月  
> 场景：SKU配置、供应链数据处理

---

## 一、字典（dict） — 就是"查表"

```python
# 创建字典：左边key，右边value
price_table = {"透明壳": 8.5, "磨砂壳": 12.0, "指环壳": 15.0}
```

### 1. 普通取值
```python
price_table["透明壳"]       # → 8.5
price_table["皮壳"]          # → ❌ 报错 KeyError，程序崩溃
```

### 2. 安全取值 .get() — 加保险，防崩溃
```python
# 格式：字典.get(要查的key, 查不到时的兜底值)
price_table.get("透明壳", 0)     # → 8.5（查到了，返回真实值）
price_table.get("皮壳", 0)       # → 0（没查到，返回兜底值）
price_table.get("皮壳", "没有")   # → "没有"（兜底值随便定）
price_table.get("皮壳")           # → None（不写第二个参数，默认None）
```

**一句话：有就返真的，没有就返备用值。**

### 3. 改值 / 新增
```python
price_table["透明壳"] = 9.0    # 改：已有的key，改value
price_table["皮壳"] = 20.0     # 增：没有的key，自动新增
```

### 4. 遍历
```python
for name, price in price_table.items():
    print(f"{name} 售价 {price}元")

# .items() 每轮吐出两个值：key 和 value
# 变量名随便起，位置决定含义：逗号左边=key，右边=value
```

### 5. 嵌套字典 — value 里面又是字典
```python
sku_config = {
    "IP16PM-CLEAR": {"品名": "透明壳", "价格": 8.5, "库存": 200}
}

# 取值：一层一层剥，连写两个方括号
sku_config["IP16PM-CLEAR"]["价格"]    # → 8.5

# 安全取嵌套值：两层 .get() 串着用
sku_config.get("IP15-RING", {}).get("价格", 0)
#           第一层兜底返回{} ↑    第二层兜底返回0 ↑
# 哪层查不到都不会崩
```

---

## 二、函数（def） — 把操作打包，起个名字

```python
# 定义函数
def check_stock(sku_name, stock):
    if stock == 0:
        print(f"⚠️ {sku_name} 缺货了！")
    else:
        print(f"✅ {sku_name} 库存{stock}个")

# 调用函数
check_stock("透明壳", 200)   # → ✅ 透明壳 库存200个
check_stock("磨砂壳", 0)     # → ⚠️ 磨砂壳 缺货了！
```

### 带返回值 — return 把结果丢回来
```python
def calc_total(price, qty):
    total = price * qty
    return total

order_amount = calc_total(8.5, 100)   # → 850.0
```

### 默认参数 — 可以不传，自动用默认值
```python
def calc_total(price, qty, discount=1.0):
    return price * qty * discount

calc_total(8.5, 100)          # → 850.0（discount 默认1.0）
calc_total(8.5, 100, 0.8)     # → 680.0（打8折）
```

### 实战函数：安全取SKU价格
```python
def get_sku_price(sku_config, sku_code):
    return sku_config.get(sku_code, {}).get("价格", 0)
```

---

## 三、列表推导式 — 一行 for 循环

### 普通写法（4行）
```python
result = []
for code, info in sku_config.items():
    if info["库存"] == 0:
        result.append(code)
```

### 列表推导式（1行）
```python
[code for code, info in sku_config.items() if info["库存"] == 0]
```

### 对照公式
```
[要什么]  [从哪遍历]                     [筛选条件]
 code     for code, info in xxx.items()   if info["库存"] == 0
```

---

## 四、易错点

| 问题 | 原因 | 正确写法 |
|------|------|----------|
| `print(result.append(x))` 返回 None | `.append()` 只管塞不返回值 | 先 `append()`，再 `print(result)` |
| `store3 = 150` 没改字典 | 只改了变量，没改字典里的值 | `sku_config["IP16PM-MATTE"]["库存"] = 150` |
| `d["不存在的key"]` 崩溃 | 普通取值查不到就报错 | 用 `d.get("key", 兜底值)` |

---

## 五、for 循环中的临时变量

```python
for code, info in sku_config.items():
#   ↑ 变量名随便起   ↑ .items() 每轮吐出 key 和 value
#   位置决定含义：第1个=key，第2个=value

# 以下三种完全等价：
for code, info in sku_config.items():
for a, b in sku_config.items():
for sku编码, 详情 in sku_config.items():
```

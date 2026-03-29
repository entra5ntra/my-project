# 钉钉API调用 学习笔记

> 学习日期：2026年3月6日  
> 场景：十二辰考勤自动化、钉钉云盘操作、群消息通知

---

## 一、API是什么？一句话理解

浏览器输入网址 → 网站返回页面给你看  
Python发请求到API地址 → 服务器返回JSON数据给你处理

**本质就是：用代码代替人去"访问网站"拿数据。**

---

## 二、核心依赖库：requests

requests 是 Python 发网络请求的库，所有API调用都靠它。

```python
import requests

# GET请求：从服务器"拿"数据（像打开网页）
resp = requests.get("https://xxx.com/api", params={"key": "value"})

# POST请求：向服务器"提交"数据（像提交表单）
resp = requests.post("https://xxx.com/api", json={"key": "value"})

# 拿到返回结果，转成字典
data = resp.json()
```

**GET vs POST 区别：**

| 方式 | 用途 | 参数位置 |
|------|------|----------|
| GET | 查询、获取数据 | 拼在网址后面（params） |
| POST | 提交、发送数据 | 放在请求体里（json） |

钉钉大部分接口用的是 POST。

---

## 三、钉钉API调用完整三步

### 第1步：拿钥匙（获取 access_token）

access_token 是临时通行证，所有后续请求都要带上它。

```python
import requests

def get_token(appkey, appsecret):
    url = "https://oapi.dingtalk.com/gettoken"
    params = {
        "appkey": appkey,
        "appsecret": appsecret
    }
    resp = requests.get(url, params=params)
    data = resp.json()
    return data["access_token"]

# 调用
token = get_token("你的AppKey", "你的AppSecret")
print(token)
```

**关键点：**
- AppKey 和 AppSecret 在钉钉开发者后台 → 应用开发 → 你的应用 → 基础信息里
- token 有效期 **2小时**，过期了重新调这个接口拿
- 这一步用的是 **GET** 请求

### 第2步：带着钥匙去取数据

token 拿到后，后续所有请求都要带上它。

**示例1：获取部门列表**

```python
def get_departments(token):
    url = "https://oapi.dingtalk.com/topapi/v2/department/listsub"
    resp = requests.post(
        url,
        params={"access_token": token},
        json={"dept_id": 1}    # 1 = 根部门（公司最顶层）
    )
    data = resp.json()
    return data.get("result", [])

depts = get_departments(token)
for d in depts:
    print(f"部门ID: {d['dept_id']}  名称: {d['name']}")
```

**示例2：获取部门下的员工列表**

```python
def get_users(token, dept_id):
    url = "https://oapi.dingtalk.com/topapi/v2/user/list"
    resp = requests.post(
        url,
        params={"access_token": token},
        json={
            "dept_id": dept_id,
            "cursor": 0,
            "size": 100
        }
    )
    data = resp.json()
    return data.get("result", {}).get("list", [])

users = get_users(token, 12345)
for u in users:
    print(f"姓名: {u['name']}  userId: {u['userid']}")
```

**示例3：获取考勤打卡记录**

```python
def get_attendance(token, user_ids, date_from, date_to):
    url = "https://oapi.dingtalk.com/attendance/list"
    resp = requests.post(
        url,
        params={"access_token": token},
        json={
            "workDateFrom": date_from,
            "workDateTo": date_to,
            "userIdList": user_ids,
            "offset": 0,
            "limit": 50
        }
    )
    data = resp.json()
    return data.get("recordresult", [])

records = get_attendance(
    token,
    ["user001", "user002"],
    "2026-03-01 00:00:00",
    "2026-03-06 23:59:59"
)
```

### 第3步：处理返回的数据

返回的就是字典和列表，用之前学的知识处理：

```python
for r in records:
    name = r["userName"]
    check_time = r["userCheckTime"]     # 打卡时间（毫秒时间戳）
    check_type = r["checkType"]         # "OnDuty"上班 / "OffDuty"下班
    print(f"{name} {check_type} {check_time}")
```

---

## 四、完整流程串起来

```python
import requests
import json

# ========== 配置 ==========
CONFIG = {
    "appkey": "dingxxxxxxxx",
    "appsecret": "xxxxxxxxxxxxxxxxxx"
}

# ========== 第1步：拿token ==========
token = get_token(CONFIG["appkey"], CONFIG["appsecret"])

# ========== 第2步：拿部门 → 拿员工 → 拿考勤 ==========
depts = get_departments(token)

all_records = []
for dept in depts:
    users = get_users(token, dept["dept_id"])
    user_ids = [u["userid"] for u in users]   # 列表推导式提取userId
    
    records = get_attendance(token, user_ids, "2026-03-01 00:00:00", "2026-03-06 23:59:59")
    all_records.extend(records)     # extend：把一个列表追加到另一个列表

# ========== 第3步：处理并保存 ==========
result = []
for r in all_records:
    result.append({
        "姓名": r["userName"],
        "打卡类型": r["checkType"],
        "打卡时间": r["userCheckTime"]
    })

# 保存到JSON文件
with open("attendance_result.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"共获取 {len(result)} 条打卡记录，已保存")
```

---

## 五、常用钉钉API接口速查

| 功能 | 接口地址 | 方法 |
|------|----------|------|
| 获取token | /gettoken | GET |
| 部门列表 | /topapi/v2/department/listsub | POST |
| 员工列表 | /topapi/v2/user/list | POST |
| 用户详情 | /topapi/v2/user/get | POST |
| 考勤打卡记录 | /attendance/list | POST |
| 发送工作通知 | /topapi/message/corpconversation/asyncsend_v2 | POST |
| 发送群消息 | /robot/send | POST |

所有接口的完整地址都是 `https://oapi.dingtalk.com` + 上面的路径。

---

## 六、返回值结构（通用格式）

钉钉API返回的JSON通常长这样：

```json
{
    "errcode": 0,
    "errmsg": "ok",
    "result": {
        "实际数据在这里..."
    },
    "request_id": "一串请求ID"
}
```

**判断是否成功：**

```python
data = resp.json()
if data["errcode"] == 0:
    result = data["result"]    # 成功，取数据
else:
    print(f"出错了：{data['errmsg']}")  # 失败，看错误信息
```

---

## 七、常见报错和解决方法

| errcode | 含义 | 解决 |
|---------|------|------|
| 0 | 成功 | — |
| 88 (sub_code 60020) | IP不在白名单 | 去开发者后台 → 应用 → 开发管理 → 加上报错里显示的IP |
| 40014 | token无效或过期 | 重新调 gettoken 获取新的 |
| 60011 | 没有调用该接口的权限 | 去应用权限管理里开通对应的权限 |
| 60012 | 接口调用超过频率限制 | 加 time.sleep() 降低调用频率 |
| 40035 | 参数不合法 | 检查传入的参数格式和字段名 |

---

## 八、config配置文件的用法

把AppKey等敏感信息放到配置文件里，不要硬写在代码中：

**config.json：**

```json
{
    "appkey": "dingxxxxxxxx",
    "appsecret": "xxxxxxxxxxxxxxxxxx",
    "date_from": "2026-03-01 00:00:00",
    "date_to": "2026-03-06 23:59:59"
}
```

**代码中读取：**

```python
import json

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

token = get_token(config["appkey"], config["appsecret"])
```

这样换环境、换时间段只改配置文件就行，不用动代码。你的考勤工具v2.0就是这么做的。

---

## 九、知识点对照表（今天学的 → API里用到的）

| 之前学的知识 | 在API调用中哪里用到 |
|-------------|-------------------|
| 字典取值 `d["key"]` | 取返回数据里的字段 |
| `.get("key", 默认值)` | 安全取返回数据，防止字段缺失崩溃 |
| 嵌套字典 | `data["result"]["list"]` 取多层数据 |
| 列表推导式 | `[u["userid"] for u in users]` 批量提取 |
| for 遍历 | 循环处理每条打卡记录 |
| json.load / json.dump | 读配置文件、保存结果 |
| 函数 def + return | 把每个API调用封装成函数复用 |
| 全局变量 vs 局部变量 | token是全局传递的，函数内部变量是局部的 |

---

## 十、调试技巧

**1. 先打印看看返回了什么：**

```python
data = resp.json()
print(json.dumps(data, ensure_ascii=False, indent=2))
# 格式化打印，中文不乱码，看清楚结构再写取值逻辑
```

**2. 用 resp.status_code 检查HTTP状态：**

```python
print(resp.status_code)   # 200=正常  其他=网络层面有问题
```

**3. 一步一步来，别一口气写完：**

```python
# 先确认token拿到了
token = get_token(appkey, appsecret)
print("token:", token[:20], "...")   # 打印前20位确认

# 再确认部门拿到了
depts = get_departments(token)
print("部门数:", len(depts))

# 再往下走...
```

跟影刀调试一样的思路：一个节点一个节点验证，不要一次性跑完。

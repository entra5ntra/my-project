# MES 逆向工程复习资料

> 基于马帮 ERP · 自动推单系统代码实例整理
> 涵盖：HTTP 请求 · 抓包能力 · sign 签名机制 · Playwright uid 获取

---

## 目录

1. [HTTP 请求是什么](#一http-请求是什么)
2. [抓包能力](#二抓包能力)
3. [sign 签名机制](#三sign-签名机制)
4. [Playwright 自动获取 uid](#四playwright-自动获取-uid)
5. [完整流程串联](#五完整流程串联)
6. [常见问题与坑](#六常见问题与坑)

---

## 一、HTTP 请求是什么

### 核心理解

> 你在浏览器里做任何操作，本质都是你的电脑给服务器**发了一封信**，服务器**回了一封信**。HTTP 就是这封信的格式规范。

### 请求的四个部分

```http
POST /router/ylk/user/submit?app_key=657123&sign=A3F9... HTTP/1.1
Host: messervice.mabangerp.com
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)...

user_id=1710820800000&uid=a3f9c2d1&user_name=shierchenPH&pa_wd=MDQwODExV1c=
```

| 部分 | 示例 | 说明 |
|------|------|------|
| 请求行 | `POST /router/ylk/user/submit` | 做什么、发到哪 |
| URL 参数 | `?app_key=657123&sign=A3F9...` | 拼在 URL 后面的参数 |
| Headers | `Content-Type`, `User-Agent` | 元信息，身份证 |
| Body | `user_id=...&uid=...` | 真正的数据正文 |

### 对应代码

```python
# URL 参数 → params=，自动拼到 URL 后面
url_params = {"app_key": APP_KEY, "sign": ..., "timestamp": timestamp}

# Body → data=urlencode()，放在请求正文
body = {"uid": _current_uid, "user_name": "shierchenPH", ...}

session.post(url, params=url_params, data=urlencode(body), headers=HEADERS)
```

### 两种 Body 格式对比

```
# 表单格式（这份代码用的）
Content-Type: application/x-www-form-urlencoded
user_id=123&uid=abc&user_name=shierchenPH

# JSON 格式（现代接口常用）
Content-Type: application/json
{"user_id": "123", "uid": "abc", "user_name": "shierchenPH"}
```

### 服务器响应

```python
res = session.post(url, ...)

# res.text   → 原始字符串（服务器返回的纯文本）
# res.json() → 解析成 Python dict，方便取值

data = res.json()
token = data.get("token")  # 取出登录成功返回的 token
```

⚠️ 如果服务器返回的不是 JSON（比如报错 HTML 页面），`res.json()` 会抛出 `JSONDecodeError`，需要加 try/catch。

### 重要细节

**User-Agent 和 Origin 不能删：**

- `User-Agent` → 伪装成真实浏览器，删掉服务器可能识别爬虫拒绝请求
- `Origin` → 服务器做跨域检查，只允许来自 `factory.mabangerp.com` 的请求

**Base64 不是加密：**

```python
pa_wd = base64.b64encode("040811WW".encode()).decode()
# → "MDQwODExV1c="

# 任何人一秒还原
base64.b64decode("MDQwODExV1c=").decode()  # → "040811WW"
```

---

## 二、抓包能力

### 核心理解

> 抓包 = 在浏览器和服务器之间架摄像头，把所有通信内容录下来。

### 工作原理

```
# 正常情况（看不到内容）
浏览器 ────────────────→ MES 服务器

# 安装 Burp 之后（中间人）
浏览器 ──→ Burp Suite ──→ MES 服务器
              ↑
           你在这里看到明文内容
```

HTTPS 本来是加密的，Burp 通过**安装自签证书**来解密：

```
浏览器信任 Burp 证书 → Burp 解密 → 查看明文 → 重新加密转发
```

不装证书的后果：`SSL handshake failed / NET::ERR_CERT_AUTHORITY_INVALID`

### 通过抓包能找到什么

这份代码里的这些内容，全部来自抓包分析：

```python
BASE_URL = "https://messervice.mabangerp.com/router/ylk"  # 接口域名+路径
APP_KEY  = "657123"                                         # URL 参数里看到的
HEADERS  = {
    "Origin": "https://factory.mabangerp.com",             # 请求头里看到的
    "Content-Type": "application/x-www-form-urlencoded",   # 请求头里看到的
}
```

光靠抓包**找不到**的：
```python
APP_SECRET = "3216bd91e938408c98d264255fe2d78f"  # 只在 JS 文件里，需要 JS 逆向
```

### 三个关键动作

**① 过滤** — 几百条请求里快速定位

```
搜索 messervice.mabangerp.com  → 只看 MES 相关请求
搜索 /user/submit              → 直接找登录接口
```

**② 对比** — 点一次按钮，看哪条请求出现了

**③ 重放** — 用 Burp Repeater 原样发一遍，返回正确结果 = 真正理解了这条请求

### 找 APP_SECRET 的方法

```
Chrome DevTools → Sources → 搜索关键词：
  app_secret / appSecret / 657123（用 app_key 反查）

常藏位置：
  /static/js/app.xxxxxx.js      ← 主业务逻辑
  /static/js/chunk-vendors.js   ← 第三方库
```

---

## 三、sign 签名机制

### 为什么需要 sign

没有 sign：任何人抓到包直接重放，随意调用接口。

有了 sign：必须用 `APP_SECRET` 计算，没有密钥造不出合法请求。

### 完整防护体系（三层）

```python
url_params = {
    "app_key":   APP_KEY,    # 第一层：身份识别（我是谁）
    "timestamp": timestamp,   # 第二层：时间戳（防重放）
    "sign":      sign,        # 第三层：HMAC-MD5（防篡改）
}
```

### 时间戳防重放原理

```
攻击者抓包拿到合法请求 → 5分钟后重放
服务器：当前时间 - 请求时间戳 > 允许误差 → 直接拒绝 ❌
```

时间戳也参与 sign 计算，所以：
```
想伪造新请求 → 需要更新 timestamp → sign 得重算 → 没有 APP_SECRET → 算不出来 ❌
```

### sign 生成算法还原

```python
def generate_sign(url_params: dict, body_params: dict) -> str:
    # 第一步：合并所有参数，加入 app_secret
    all_params = {**url_params, "app_secret": APP_SECRET, **body_params}

    # 第二步：过滤空值（服务器端也过滤，双方参数集合必须一致）
    all_params = {k: v for k, v in all_params.items() if str(v) != ""}

    # 第三步：按 key 字母排序，拼成 key1val1key2val2 格式
    sorted_str = "".join(f"{k}{v}" for k, v in sorted(all_params.items()))

    # 第四步：HMAC-MD5，密钥是 APP_SECRET
    mac = hmac.new(APP_SECRET.encode(), sorted_str.encode(), hashlib.md5)

    # 第五步：结果转大写
    return mac.hexdigest().upper()
```

**为什么必须排序？**

客户端和服务器必须用完全相同的方式生成 sign，不排序就可能有无数种拼法，双方结果永远对不上。

**HMAC vs 普通 MD5：**

```python
# 普通 MD5 —— 知道算法就能伪造
md5("app_key657123timestamp1710820800")

# HMAC-MD5 —— 还需要密钥，光知道算法不够
hmac(APP_SECRET, "app_key657123timestamp1710820800")
```

### 从 JS 逆向找算法

在 DevTools 里搜 `sign`，找到类似：

```javascript
function generateSign(params) {
    let keys = Object.keys(params).sort()          // 排序
    let str = keys.map(k => k + params[k]).join('') // 拼接
    return CryptoJS.HmacMD5(str, APP_SECRET).toString().toUpperCase()
}
```

看到 `HmacMD5` → Python 用 `hmac` 库；看到 `sort()` → 需要排序。

### 三层防护缺一不可

| 缺少 | 后果 |
|------|------|
| 没有 app_key | 服务器不知道是谁调用 |
| 没有 timestamp | 抓包可以无限重放 |
| 没有 sign | 任何人可以篡改参数 |

---

## 四、Playwright 自动获取 uid

### 为什么 uid 难搞

uid 每隔几小时变化一次，普通方案：

```
抓包 → 硬编码 uid → 几小时后失效 → 程序报错 ❌
JS 逆向 uid 生成算法 → 可能跟设备指纹/浏览器环境绑定 → 成本极高 ❌
```

### 解决思路：不逆向，直接"偷"

```
不理解 uid 怎么生成
→ 让真实浏览器跑一遍登录
→ 在它发出请求的瞬间把 uid 截走
→ 拿来直接用 ✅
```

### 代码逐步解读

```python
def get_uid_via_playwright():
    uid_result = []
    temp_dir = tempfile.mkdtemp()  # 临时目录，用完删掉不留痕迹

    with sync_playwright() as p:
        # 第一步：启动无头浏览器（后台运行，看不到界面）
        browser = p.chromium.launch_persistent_context(
            user_data_dir=temp_dir,
            headless=True,    # True=后台静默  False=弹出窗口（调试用）
            channel="chrome", # 用真实 Chrome，服务器识别不出是爬虫
        )
        page = browser.new_page()

        # 第二步：监听所有网络请求，拦截登录接口
        def handle_request(request):
            if 'user/submit' in request.url:         # 只关心登录接口
                post_data = request.post_data or ""
                for part in post_data.split("&"):    # 解析 Body
                    if part.startswith("uid="):      # 找到 uid
                        uid_result.append(part.split("=", 1)[1])

        page.on("request", handle_request)  # 注册监听器

        # 第三步：打开页面，自动填写账号密码点登录
        page.goto("https://factory.mabangerp.com")
        inputs = page.query_selector_all('input')
        inputs[0].fill(WAREHOUSES[0]["user_name"])
        inputs[1].fill(WAREHOUSES[0]["password"])
        page.click('button[type="submit"]')

        # 第四步：等待 uid 出现（最多30秒）
        for _ in range(30):
            if uid_result:
                break
            time.sleep(1)

        browser.close()

    _current_uid = uid_result[0]  # 存到全局变量供后续使用
```

### 为什么用 WAREHOUSES[0] 的账号

uid 绑定的是**客户端环境**（这台机器+这个浏览器），不绑定账号本身。同一台机器上用哪个账号登录拿到的 uid 都一样，其他仓库可以直接复用。

### headless=True vs False

| 模式 | 场景 |
|------|------|
| `headless=True` | 正常运行，后台静默，看不到界面 |
| `headless=False` | 调试排错，弹出真实窗口，能亲眼看到自动操作过程 |

### 潜在风险：输入框定位脆弱

当前写法依赖顺序，非常脆弱：

```python
# ❌ 脆弱写法：依赖"第一个是账号，第二个是密码"
inputs[0].fill(user_name)
inputs[1].fill(password)

# ✅ 健壮写法：通过属性精准定位
page.fill('input[placeholder="账号"]', user_name)
page.fill('input[placeholder="密码"]', password)
# 或
page.fill('input[name="username"]', user_name)
page.fill('input[name="password"]', password)
```

页面改版加了输入框，顺序变了，旧写法会填错位置，且**不报错**，只会静默失败。

### uid 刷新时机

```python
# 时机1：程序启动时获取一次
get_uid_via_playwright()

# 时机2：登录失败时自动重试
if attempt == 0:
    get_uid_via_playwright()  # uid 过期了，刷新再试
```

---

## 五、完整流程串联

### 代码整体架构

```
main()
├── 启动时获取 uid（Playwright）
└── 无限循环，每30秒检查一次时间
    └── 到时间 → push_warehouse()
        ├── 1. login()             登录拿 Token
        ├── 2. get_pending_tasks() 查待审任务
        └── 3. 遍历批次
            ├── lock_stock()       锁库存（可选，超时递增重试）
            └── create_batch()     创建批次推单
                └── send_dingtalk() 结果通知
```

### 从抓包到自动化的完整链路

```
抓包
 └─→ 发现接口地址、参数结构、Header 要求
      └─→ JS 逆向
           └─→ 找到 APP_SECRET、sign 算法
                └─→ Python 还原 sign 生成逻辑
                     └─→ Playwright 解决 uid 动态问题
                          └─→ 组装完整请求，自动化执行
```

### 定时调度逻辑

```python
# 手写轮询，不依赖第三方库
while True:
    now = time.localtime()

    # 凌晨3点重置当天推单状态
    if today != last_reset_date and current_hour >= 3:
        pushed_today = {w["name"]: False for w in WAREHOUSES}

    # 到时间就推
    for warehouse in WAREHOUSES:
        if current_hour == warehouse["push_hour"] and current_minute >= warehouse["push_minute"]:
            push_warehouse(warehouse)

    time.sleep(30)  # 每30秒检查一次
```

三个仓库推单时间：

| 仓库 | 时间 |
|------|------|
| 菲律宾 | 07:10 |
| 东莞 | 07:45 |
| 越南 | 08:10 |

---

## 六、常见问题与坑

### sign 对不上的排查思路

```
1. 检查参数是否都参与了计算（特别是 app_secret 本身）
2. 检查空值是否过滤（双方规则必须一致）
3. 检查排序方式（大小写敏感？）
4. 检查编码（字符串 encode 的方式）
5. 检查大小写（结果是否要 upper()）
```

### 锁库存超时处理

```python
# 超时时间递增，给服务器更多处理时间
timeouts = [180, 300, 600]  # 3min → 5min → 10min
waits    = [30, 60]          # 失败后等待再重试
```

### 安全风险（注意事项）

| 问题 | 现状 | 建议 |
|------|------|------|
| 密码明文 | 写死在代码里 | 放到 `.env` 文件 |
| APP_SECRET 明文 | 写死在代码里 | 放到 `.env` 文件 |
| 钉钉 Webhook | 写死在代码里 | 放到 `.env` 文件 |
| Token 过期 | 没有检测 | 加过期时间判断 |
| uid 长期不刷新 | 只失败时刷新 | 加定时刷新（如每6小时）|

### .env 文件使用方式

```python
# .env 文件
APP_KEY=657123
APP_SECRET=3216bd91e938408c98d264255fe2d78f

# Python 读取
from dotenv import load_dotenv
import os
load_dotenv()
APP_SECRET = os.getenv("APP_SECRET")
```

---

## 七、核心概念速查

| 概念 | 一句话理解 |
|------|-----------|
| HTTP 请求 | 客户端发给服务器的一封信，有固定格式 |
| Headers | 信封上的元信息，伪装浏览器身份用 |
| Body | 信的正文，真正的业务数据 |
| Base64 | 编码不是加密，一秒可逆 |
| 抓包 | 在通信中间架摄像头，看明文内容 |
| MITM | 中间人，Burp 解密 HTTPS 的原理 |
| sign | 用密钥对参数签名，防篡改防伪造 |
| timestamp | 时间戳，防止合法请求被重放 |
| HMAC-MD5 | 带密钥的 MD5，没有密钥就算不出结果 |
| uid | 绑定客户端环境，有时效性 |
| Playwright | 控制真实浏览器，用来获取难逆向的参数 |
| headless | True=后台静默，False=弹窗调试 |

---

*整理自实战代码：马帮 ERP MES 三仓库自动推单系统*

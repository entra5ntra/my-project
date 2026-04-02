# DrissionPage 学习指南

> 从零开始学习 DrissionPage 浏览器自动化，基于 automationexercise.com 实战练习整理。

---

## 一、安装与环境

```bash
pip install DrissionPage
```

确认版本：

```python
import DrissionPage
print(DrissionPage.__version__)
```

---

## 二、核心概念

DrissionPage 有两种模式：

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| `ChromiumPage` | 控制真实浏览器，能处理 JS 渲染 | 店小秘上架、登录操作 |
| `SessionPage` | 用 requests 发请求，速度快 | 纯接口调用、不需要渲染的页面 |

日常自动化主要用 `ChromiumPage`。

---

## 三、启动浏览器

### 基本启动

```python
from DrissionPage import ChromiumPage

page = ChromiumPage()
page.get('https://automationexercise.com')
```

### 设置加载模式（加速页面加载）

```python
from DrissionPage import ChromiumPage, ChromiumOptions

co = ChromiumOptions()
co.set_load_mode('eager')  # DOM加载完就行，不等图片/CSS
page = ChromiumPage(co)
```

三种加载模式：

| 模式 | 说明 | 速度 |
|------|------|------|
| `'normal'` | 等所有资源加载完 | 最慢（默认） |
| `'eager'` | DOM 加载完就行，不等图片和样式 | 推荐 |
| `'none'` | 发出请求就不等了 | 最快，但元素可能还没出来 |

### 设置超时时间

```python
page.set.timeouts(base=30, page_load=60)
```

---

## 四、元素定位（核心技能）

### 4.1 定位方式一览

```python
# 1. 直接用文本找（DrissionPage 特色，最简单）
page.ele('Signup / Login')

# 2. 精确匹配文本
page.ele('@@text()=登录')

# 3. 用 CSS 选择器
page.ele('css:#login-btn')              # 用 id
page.ele('css:.nav-item')               # 用 class
page.ele('css:input[name="email"]')     # 用属性
page.ele('css:button[data-qa="signup-button"]')  # 用 data-qa

# 4. 用 tag 名 + 属性（DrissionPage 特有语法）
page.ele('tag:a')                       # 找第一个 a 标签
page.ele('tag:input@type=text')         # 找 type=text 的 input
page.ele('tag:button@name=submit')      # 找 name=submit 的按钮
page.ele('tag:input@value=Mr')          # 找 value=Mr 的 input

# 5. 用 xpath
page.ele('xpath://a[contains(text(),"Login")]')
page.ele('xpath://input[@name="email"]')
```

### 4.2 定位优先级（推荐顺序）

遇到重复元素时，按这个优先级选择定位方式：

```
data-qa / data-testid  >  id  >  name + 上下文  >  CSS 层级选择器
```

`data-qa` 是开发者专门留给自动化用的标识，最稳定也最唯一。

### 4.3 处理重复元素

当页面有多个相似元素时（比如两个 `name="email"` 的输入框），用更精确的属性区分：

```python
# ❌ 不精确，可能找错
page.ele('css:input[name="email"]')

# ✅ 用 data-qa 精确定位
page.ele('css:input[data-qa="login-email"]')    # 登录表单的
page.ele('css:input[data-qa="signup-email"]')   # 注册表单的
```

### 4.4 调试定位：查看元素 HTML

```python
ele = page.ele('css:button[data-qa="signup-button"]')
print(ele.html)      # 打印元素的完整 HTML
print(ele.text)      # 打印元素的文本内容
print(ele.attr('href'))  # 打印某个属性值
```

### 4.5 浏览器中查看元素属性

两种方式：
1. 对着目标元素 **右键 → 检查（Inspect）**，DevTools 自动定位到 HTML
2. 按 **F12** 打开 DevTools，点左上角 🔍 箭头图标，再点页面上的元素

---

## 五、元素操作

### 5.1 点击

```python
# 普通点击
page.ele('Signup / Login').click()

# JS 点击（元素被遮挡时用）
page.ele('css:button[data-qa="signup-button"]').click(by_js=True)
```

### 5.2 输入

```python
page.ele('css:#password').input('123456')
page.ele('css:input[name="company"]').input('英派特')
page.ele('css:input[data-qa="first_name"]').input('张')
```

### 5.3 操作判断依据

看元素的 `type` 属性来决定用 `click()` 还是 `input()`：

| type 属性 | 操作 | 示例 |
|-----------|------|------|
| `text` | `.input()` | 文本输入框 |
| `password` | `.input()` | 密码框 |
| `email` | `.input()` | 邮箱框 |
| `submit` | `.click()` | 提交按钮 |
| `radio` | `.click()` | 单选按钮 |
| `checkbox` | `.click()` | 复选框 |
| `button` | `.click()` | 普通按钮 |

### 5.4 下拉框选择（`<select>` 标签）

```python
# 按显示文本选
page.ele('css:#country').select.by_text('United States')

# 按 value 值选
page.ele('css:#days').select.by_value('15')

# 日期选择示例
page.ele('css:#days').select.by_value('15')
page.ele('css:#months').select.by_text('March')
page.ele('css:#years').select.by_value('1999')
```

### 5.5 获取信息

```python
text = page.ele('css:.title').text           # 获取文本
href = page.ele('tag:a').attr('href')        # 获取属性
html = page.ele('css:#myid').html            # 获取完整 HTML
```

---

## 六、等待机制

```python
# 等待文档加载完成
page.wait.doc_loaded()

# 等待指定时间
page.wait(1)  # 等1秒

# 等待元素出现（设置超时时间）
page.ele('css:.success', timeout=10)

# 先滚动到元素位置，再点击
ele = page.ele('css:button[data-qa="create-account"]')
ele.scroll.to_see()
ele.click()
```

---

## 七、常见问题与解决

### 7.1 点击不生效

```python
# 方式1：JS 点击，绕过遮挡
page.ele('css:button').click(by_js=True)

# 方式2：滚动到元素位置再点
ele = page.ele('css:button')
ele.scroll.to_see()
ele.click()

# 方式3：等一下再点
page.wait(1)
page.ele('css:button').click()
```

### 7.2 找不到元素

```python
# 增加等待时间
page.ele('css:.target', timeout=15)

# 确认页面是否加载完成
page.wait.doc_loaded()
```

### 7.3 页面加载太慢

```python
co = ChromiumOptions()
co.set_load_mode('eager')  # 不等图片和样式
page = ChromiumPage(co)
```

---

## 八、实战案例：automationexercise.com 自动注册

```python
from DrissionPage import ChromiumPage, ChromiumOptions

co = ChromiumOptions()
co.set_load_mode('eager')
page = ChromiumPage(co)

# 1. 访问网站
page.get('https://automationexercise.com')

# 2. 点击 Signup / Login
page.ele('Signup / Login').click()

# 3. 填写注册信息
page.ele('css:input[data-qa="signup-name"]').input('ertan')
page.ele('css:input[data-qa="signup-email"]').input('2710437252@qq.com')
page.ele('css:button[data-qa="signup-button"]').click(by_js=True)

# 4. 等待详情页加载
page.wait.doc_loaded()

# 5. 填写详细信息
page.ele('css:#id_gender1').click()                          # 选性别
page.ele('css:input[name="password"]').input('1479447894')   # 密码
page.ele('css:#days').select.by_value('15')                  # 日
page.ele('css:#months').select.by_text('March')              # 月
page.ele('css:#years').select.by_value('1999')               # 年
page.ele('css:#newsletter').click()                          # 订阅
page.ele('css:#optin').click()                               # 接收优惠
page.ele('css:input[data-qa="first_name"]').input('张')
page.ele('css:input[data-qa="last_name"]').input('无忌')
page.ele('css:#company').input('英派特')
page.ele('css:input[data-qa="address"]').input('深圳坂田')
page.ele('css:#country').select.by_text('Canada')
page.ele('css:input[data-qa="state"]').input('guo')
page.ele('css:input[data-qa="city"]').input('li')
page.ele('css:input[data-qa="zipcode"]').input('234574')
page.ele('css:input[data-qa="mobile_number"]').input('19304802857')

# 6. 提交注册
page.ele('css:button[data-qa="create-account"]').click(by_js=True)

# 7. 验证注册结果
page.wait.doc_loaded()
if page.ele('Account Created!'):
    print('注册成功！')
```

---

## 九、进阶技能（店小秘上架会用到）

### 9.1 监听网络请求（拦截 API 响应）

```python
page.listen.start('shopeeProduct')    # 监听包含关键词的请求
# ... 执行页面操作 ...
packet = page.listen.wait()           # 等待请求出现
print(packet.response.body)           # 获取响应数据
```

### 9.2 获取 Cookie（用于 requests 调接口）

```python
# 从 DrissionPage 提取 cookie
cookies = page.cookies()
for cookie in cookies:
    print(cookie['name'], cookie['value'])

# 塞进 requests.Session
import requests
session = requests.Session()
for cookie in page.cookies():
    session.cookies.set(cookie['name'], cookie['value'])
```

### 9.3 非标准下拉框（div 模拟的）

店小秘里可能遇到非标准下拉框，处理方式：

```python
# 先点击展开下拉框
page.ele('css:.select-trigger').click()
page.wait(0.5)
# 再点击具体选项
page.ele('text:目标选项文字').click()
```

### 9.4 文件上传

```python
# 标准文件上传控件
page.ele('css:input[type="file"]').input(r'C:\images\product.jpg')

# 如果上传控件隐藏了，用 JS 让它可见
page.run_js('document.querySelector("input[type=file]").style.display="block"')
page.ele('css:input[type="file"]').input(r'C:\images\product.jpg')
```

### 9.5 心跳保活（保持 Session 不过期）

```python
import threading, time

def keep_alive(session):
    while True:
        session.post('https://www.dianxiaomi.com/api/crawl/getUnprocessedCount.json')
        time.sleep(300)  # 每5分钟一次

threading.Thread(target=keep_alive, args=(session,), daemon=True).start()
```

---

## 十、混合方案：DrissionPage + requests

最佳实践是两者结合使用：

```python
from DrissionPage import ChromiumPage
import requests

# 1. 用 DrissionPage 登录，拿 Cookie
page = ChromiumPage()
page.get('https://www.dianxiaomi.com')
# ... 登录操作 ...

# 2. 提取 Cookie 到 requests
session = requests.Session()
for cookie in page.cookies():
    session.cookies.set(cookie['name'], cookie['value'])

# 3. 用 requests 直接调接口（速度快10倍）
resp = session.post(
    'https://www.dianxiaomi.com/api/shopeeProduct/pageList.json',
    data={
        'pageNo': 1,
        'pageSize': 100,
        'shopId': -1,
        'dxmState': 'online',
        'productState': 'NORMAL',
    }
)
print(resp.json())
```

---

## 附录：速查表

| 需求 | 代码 |
|------|------|
| 打开页面 | `page.get('url')` |
| 用文本找元素 | `page.ele('按钮文字')` |
| 用 CSS 找元素 | `page.ele('css:#id')` |
| 用 tag + 属性找 | `page.ele('tag:input@name=email')` |
| 点击 | `.click()` |
| JS 点击 | `.click(by_js=True)` |
| 输入 | `.input('内容')` |
| 下拉框按文本选 | `.select.by_text('选项')` |
| 下拉框按值选 | `.select.by_value('值')` |
| 获取文本 | `.text` |
| 获取属性 | `.attr('href')` |
| 获取 HTML | `.html` |
| 等待加载 | `page.wait.doc_loaded()` |
| 等待N秒 | `page.wait(2)` |
| 带超时找元素 | `page.ele('css:.x', timeout=10)` |
| 滚动到元素 | `ele.scroll.to_see()` |
| 文件上传 | `.input(r'文件路径')` |
| 监听请求 | `page.listen.start('关键词')` |
| 获取 Cookie | `page.cookies()` |

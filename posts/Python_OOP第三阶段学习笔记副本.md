# Python OOP 第三阶段学习笔记
### 魔术方法、类方法、静态方法、综合项目

---

## 1. 魔术方法（Magic Methods）

魔术方法的特点是**左右各两个下划线**，Python 会在特定情况下自动调用。

你已经用过一个魔术方法了：`__init__`！

---

### `__str__` — 控制 print 时显示什么

```python
class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"狗狗：{self.name}，{self.age}岁"

dog = Dog("小黑", 3)
print(dog)  # 狗狗：小黑，3岁
```

没有 `__str__` 时：`<__main__.Dog object at 0x...>`（一串看不懂的东西）

---

### `__len__` — 让对象支持 len()

```python
class Bookshelf:
    def __init__(self, owner, books):
        self.owner = owner
        self.books = books

    def __len__(self):
        return len(self.books)

shelf = Bookshelf("小明", ["西游记", "红楼梦", "水浒传"])
print(len(shelf))  # 3
```

**注意：** `__len__` 适合用在有"多个元素"的属性上，比如列表，不适合用在单个数字上。

---

## 2. 类方法 & 静态方法

### 三种方法对比

| 方法类型 | 装饰器 | 第一个参数 | 调用方式 | 使用场景 |
|--------|--------|-----------|---------|---------|
| 普通方法 | 无 | `self` | `对象.方法()` | 操作某个对象的数据 |
| 类方法 | `@classmethod` | `cls` | `类.方法()` | 操作整个类共享的数据 |
| 静态方法 | `@staticmethod` | 无 | `类.方法()` | 只是个工具，跟类和对象都没关系 |

---

### 记忆方法

> - 需要某个对象的数据？→ **普通方法**
> - 需要整个类的共享数据？→ **类方法**
> - 只是个计算工具？→ **静态方法**

---

### 代码示例

```python
class Student:
    school = "光明中学"  # 类属性，所有学生共享

    def __init__(self, name, score):
        self.name = name
        self.score = score

    def introduce(self):           # 普通方法
        print(f"我叫{self.name}")

    @classmethod
    def get_school(cls):           # 类方法
        print(f"学校：{cls.school}")

    @staticmethod
    def is_pass(score):            # 静态方法
        if score >= 60:
            print("及格")
        else:
            print("不及格")

student = Student("小明", 85)
student.introduce()          # 普通方法，用对象调用
Student.get_school()         # 类方法，用类调用
Student.is_pass(85)          # 静态方法，用类调用
Student.is_pass(student.score)  # 用学生自己的成绩判断
```

---

## 3. 综合项目：图书管理系统

```python
class Book:
    def __init__(self, title, author, price):
        self.title = title
        self.author = author
        self.price = price

    def __str__(self):
        return f"《{self.title}》- {self.author} - {self.price}元"


class Library:
    def __init__(self, name):
        self.name = name
        self.books = []    # 书架，初始为空列表

    def add_book(self, book):
        self.books.append(book)  # 往书架上加一本书

    def show_all(self):
        for book in self.books:  # 遍历书架上每本书
            print(book)          # 自动调用Book的__str__

    def __len__(self):
        return len(self.books)   # 书架上有几本书


# 创建两本书
book1 = Book("西游记", "吴承恩", 30)
book2 = Book("红楼梦", "曹雪芹", 45)

# 创建图书馆
library = Library("光明图书馆")

# 添加书
library.add_book(book1)
library.add_book(book2)

# 打印所有书
library.show_all()

# 打印藏书数量
print(len(library))
```

输出：
```
《西游记》- 吴承恩 - 30元
《红楼梦》- 曹雪芹 - 45元
2
```

---

### 综合项目逐行解释

**Book 类** — 一本书的模板
- `__init__` — 记录书名、作者、价格
- `__str__` — 控制打印时显示的格式

**Library 类** — 图书馆的模板
- `self.books = []` — 书架从空开始，不需要外部传入
- `add_book` — 用 `append` 往书架（列表）里加书
- `show_all` — 用 `for` 循环打印每本书
- `__len__` — 返回书架上书的数量

---

## 练习题参考答案

**练习8：Bookshelf**
```python
class Bookshelf:
    def __init__(self, owner, books):
        self.owner = owner
        self.books = books

    def __str__(self):
        return f"{self.owner}的书架"

    def __len__(self):
        return len(self.books)

bookshelf = Bookshelf("小明", ["西游记", "红楼梦", "水浒传"])
print(bookshelf)       # 小明的书架
print(len(bookshelf))  # 3
```

**练习9：Student 类方法和静态方法**
```python
class Student:
    school = "光明中学"

    def __init__(self, name, score):
        self.name = name
        self.score = score

    @classmethod
    def get_school(cls):
        print(f"学校：{cls.school}")

    @staticmethod
    def is_pass(score):
        if score >= 60:
            print("及格")
        else:
            print("不及格")

Student.get_school()
Student.is_pass(75)   # 及格
Student.is_pass(45)   # 不及格
```

---

## 常见错误总结

| 错误 | 原因 | 解决方法 |
|------|------|----------|
| `__str__` 缩进错误 | 写进了 `__init__` 里 | 和 `__init__` 同级 |
| `add_book` 写成 `__add_book` | 多加了 `__` | 普通方法不需要 `__` |
| `for` 循环少了 `:` | 手误 | `for book in self.books:` |
| `self.book` 少了 `s` | 拼写错误 | `self.books` |
| `print(len(obj))` 忘了 `print` | 只计算没打印 | 套上 `print()` |

---

## OOP 三阶段总结

| 阶段 | 内容 |
|------|------|
| 第一阶段 | `class`、`__init__`、`self`、属性和方法、修改属性 |
| 第二阶段 | 继承、`super()`、封装、多态 |
| 第三阶段 | 魔术方法、类方法、静态方法、综合项目 |

🎉 **OOP 全部学完！**

# Python OOP 面向对象编程学习笔记

---

## 第一阶段：基础

### 1. 什么是 Class（类）？

Class 是一个**模板**，用模板可以创建出很多具体的对象。

- 模板 = `class`（类）
- 用模板创建出来的具体东西 = **对象（object）**

---

### 2. 第一个 Class

```python
class Car:
    def __init__(self, brand, color):
        self.brand = brand   # 属性：品牌
        self.color = color   # 属性：颜色

    def start(self):
        print(f"{self.brand} 启动了！")

car1 = Car("Toyota", "红色")
car2 = Car("BMW", "黑色")

car1.start()   # Toyota 启动了！
car2.start()   # BMW 启动了！
```

---

### 3. 三个关键点

| 概念 | 说明 |
|------|------|
| `__init__` | 创建对象时自动运行，用来设置初始属性（注意左右各**两个**下划线） |
| `self` | 代表"这个对象自己"，每个方法第一个参数都要写它 |
| `self.属性` | 把数据绑定到对象上，其他方法也能使用 |

---

### 4. 修改属性

**方法一：直接修改**
```python
dog1 = Dog("小黑", 3)
dog1.age = 5     # 直接修改
```

**方法二：在方法里修改**
```python
def birthday(self):
    self.age = self.age + 1
    print(f"{self.name}过生日了，现在{self.age}岁！")
```

---

### 练习题参考答案

**练习1：Dog class**
```python
class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def bark(self):
        print(f"{self.name}说：汪汪！")

dog1 = Dog("黄狗", 3)
dog2 = Dog("黑狗", 5)
dog1.bark()
dog2.bark()
```

**练习2：新增 introduce() 方法**
```python
class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def bark(self):
        print(f"{self.name}说：汪汪！")

    def introduce(self):
        print(f"我叫{self.name}，我今年{self.age}岁")

dog1 = Dog("黄狗", 3)
dog1.bark()
dog1.introduce()
```

**练习3：BankAccount class**
```python
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance = self.balance + amount
        print(f"存入{amount}元，当前余额是{self.balance}元")

    def withdraw(self, amount):
        self.balance = self.balance - amount
        print(f"取出{amount}元，当前余额是{self.balance}元")

account = BankAccount("张三")
account.deposit(1000)
account.withdraw(300)
print(account.balance)
```

---

## 第二阶段：核心概念

### 1. 继承（Inheritance）

子类自动拥有父类的所有属性和方法，还可以加自己独有的。

```python
# 父类
class Animal:
    def __init__(self, name):
        self.name = name

    def eat(self):
        print(f"{self.name}在吃饭")

# 子类，继承Animal
class Dog(Animal):
    def bark(self):
        print(f"{self.name}：汪汪！")

class Cat(Animal):
    def meow(self):
        print(f"{self.name}：喵喵！")

dog = Dog("小黑")
dog.eat()    # 从Animal继承来的
dog.bark()   # Dog自己的方法
```

---

### 2. super()

`super()` 用于调用父类的方法，避免重复写代码。

```python
class Animal:
    def __init__(self, name):
        self.name = name

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)  # 调用父类的__init__处理name
        self.breed = breed      # 自己只管新增的属性

dog = Dog("小黑", "柴犬")
print(dog.name)   # 小黑
print(dog.breed)  # 柴犬
```

---

### 3. 封装（Encapsulation）

属性名前加 `__`，外部就无法直接读取或修改，只能通过方法来操作。

```python
class BankAccount:
    def __init__(self, owner):
        self.owner = owner
        self.__balance = 0      # 私有属性

    def deposit(self, amount):
        self.__balance += amount

    def get_balance(self):
        return self.__balance

account = BankAccount("张三")
account.deposit(1000)
print(account.get_balance())  # ✅ 1000
print(account.__balance)      # ❌ 报错！
```

---

### 练习题参考答案

**练习4：Vehicle 继承**
```python
class Vehicle:
    def __init__(self, brand):
        self.brand = brand

    def move(self):
        print(f"{self.brand}正在移动")

class Car(Vehicle):
    def honk(self):
        print(f"{self.brand}：嘀嘀！")

class Boat(Vehicle):
    def sail(self):
        print(f"{self.brand}正在航行")

car = Car("宝马")
boat = Boat("邮轮")
car.honk()
boat.sail()
car.move()
boat.move()
```

**练习5：super() 练习**
```python
class Vehicle:
    def __init__(self, brand, speed):
        self.brand = brand
        self.speed = speed

class Car(Vehicle):
    def __init__(self, brand, speed, doors):
        super().__init__(brand, speed)
        self.doors = doors

    def honk(self):
        print(f"{self.brand}：嘀嘀！")

    def info(self):
        print(f"{self.brand}，速度{self.speed}，{self.doors}个车门")

car = Car("宝马", 160, 4)
car.info()
car.honk()
```

**练习6：封装练习**
```python
class Student:
    def __init__(self, name):
        self.name = name
        self.__score = 0

    def set_score(self, score):
        if score < 0 or score > 100:
            print("成绩无效！")
        else:
            self.__score = score

    def get_score(self):
        return self.__score

stu = Student("小明")
stu.set_score(85)
print(stu.get_score())   # 85
stu.set_score(150)       # 成绩无效！
print(stu.get_score())   # 85
```

---

## 常见错误总结

| 错误 | 原因 | 解决方法 |
|------|------|----------|
| `__init__` 写成 `_init_` | 下划线数量不对 | 左右各**两个**下划线 |
| `{name}` 写成 `{self.name}` | 忘记加 self | class 内部访问属性要用 `self.属性` |
| `Dog()` takes no arguments | `__init__` 写错 | 检查 `__init__` 的下划线 |
| 直接用 `ClassName.method()` | 没有先创建对象 | 先 `obj = ClassName()` 再 `obj.method()` |
| 子类忘记继承父类 | `class Car:` 而不是 `class Car(Vehicle):` | 括号里写父类名 |

---

*继续学习：第二阶段还剩「多态（Polymorphism）」*

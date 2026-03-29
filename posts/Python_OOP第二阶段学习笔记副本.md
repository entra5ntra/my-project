# Python OOP 第二阶段学习笔记
### 继承、super()、封装、多态

---

## 1. 继承（Inheritance）

子类自动拥有父类的所有属性和方法，还可以加自己独有的。

- 父类 = 通用模板
- 子类 = 在父类基础上扩展

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def eat(self):
        print(f"{self.name}在吃饭")

class Dog(Animal):
    def bark(self):
        print(f"{self.name}：汪汪！")

class Cat(Animal):
    def meow(self):
        print(f"{self.name}：喵喵！")

dog = Dog("小黑")
dog.eat()    # ← 从Animal继承来的
dog.bark()   # ← Dog自己的方法
```

**核心：** 子类名后面括号里写父类名 `class Dog(Animal):`

---

## 2. super()

`super()` 用于调用父类的方法，避免重复写代码。

**不用 super() 的问题：**
```python
class Dog(Animal):
    def __init__(self, name, breed):
        self.name = name   # 重复写了父类的代码！
        self.breed = breed
```

**用 super() 解决：**
```python
class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)  # 让父类处理name
        self.breed = breed      # 自己只管新增的属性

dog = Dog("小黑", "柴犬")
print(dog.name)   # 小黑
print(dog.breed)  # 柴犬
```

**核心：** `super().__init__()` = 调用父类的 `__init__`

---

## 3. 封装（Encapsulation）

属性名前加 `__`，外部无法直接访问，只能通过方法操作。

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
print(account.__balance)      # ❌ 报错！外部不能直接访问
```

**核心：** 属性名前加 `__` = 私有属性，外部无法直接读写

---

## 4. 多态（Polymorphism）

同一个方法名，不同子类有不同的实现。

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        pass  # 父类不实现，留给子类

class Dog(Animal):
    def speak(self):
        print(f"{self.name}：汪汪！")

class Cat(Animal):
    def speak(self):
        print(f"{self.name}：喵喵！")

class Duck(Animal):
    def speak(self):
        print(f"{self.name}：嘎嘎！")

animals = [Dog("小黑"), Cat("小白"), Duck("唐老鸭")]
for animal in animals:
    animal.speak()  # 同一个方法，不同的结果
```

输出：
```
小黑：汪汪！
小白：喵喵！
唐老鸭：嘎嘎！
```

**核心：** `pass` = 占位符，什么都不做，留给子类去实现

---

## 练习题参考答案

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

**练习7：多态练习**
```python
class Shape:
    def __init__(self, color):
        self.color = color

    def area(self):
        pass

class Circle(Shape):
    def __init__(self, color, radius):
        super().__init__(color)
        self.radius = radius

    def area(self):
        print(f"圆形面积是：{self.radius * self.radius * 3.14}")

class Rectangle(Shape):
    def __init__(self, color, width, height):
        super().__init__(color)
        self.width = width
        self.height = height

    def area(self):
        print(f"长方形面积是：{self.width * self.height}")

class Triangle(Shape):
    def __init__(self, color, base, height):
        super().__init__(color)
        self.base = base
        self.height = height

    def area(self):
        print(f"三角形面积是：{self.base * self.height / 2}")

shapes = [Circle("红色", 3), Rectangle("蓝色", 3, 4), Triangle("绿色", 5, 6)]
for shape in shapes:
    shape.area()
```

---

## 常见错误总结

| 错误 | 原因 | 解决方法 |
|------|------|----------|
| 子类忘记继承父类 | `class Dog:` | 改成 `class Dog(Animal):` |
| 子类缩进错误 | 子类写进了另一个类里面 | 确保每个 class 顶格写 |
| 创建对象时传入类而不是值 | `Circle(Shape, 3)` | 改成 `Circle("红色", 3)` |
| 私有属性外部直接访问 | `account.__balance` | 用 `get_balance()` 方法访问 |
| `self.heigth` 拼写错误 | 手误 | 改成 `self.height` |

---

## 第二阶段总结

| 概念 | 关键语法 | 作用 |
|------|----------|------|
| 继承 | `class Dog(Animal):` | 子类复用父类的代码 |
| super() | `super().__init__()` | 调用父类的构造方法 |
| 封装 | `self.__属性` | 保护数据，不让外部随意修改 |
| 多态 | 子类重写同名方法 | 同一方法，不同表现 |

---

*下一阶段：魔术方法、类方法、静态方法*

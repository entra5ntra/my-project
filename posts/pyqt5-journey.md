---
date: 2025-12-20
tag: Python
title: 从零开始的 PyQt5 GUI 之旅
---

## 为什么要做 GUI

脚本做好之后，同事说看不懂命令行，希望有个界面能点点就完事。于是开始学 PyQt5。

## 安装

```bash
pip install PyQt5
```

## 最基础的窗口

```python
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle('我的第一个窗口')
window.resize(400, 300)

layout = QVBoxLayout()
layout.addWidget(QLabel('Hello, PyQt5!'))
window.setLayout(layout)

window.show()
sys.exit(app.exec_())
```

## 文件选择对话框

这个是最常用的功能——让用户选一个 Excel 文件：

```python
from PyQt5.QtWidgets import QFileDialog

def select_file(self):
    path, _ = QFileDialog.getOpenFileName(
        self,
        '选择文件',
        '',
        'Excel 文件 (*.xlsx *.xls)'
    )
    if path:
        self.file_path = path
        self.label.setText(f'已选择: {path}')
```

## 进度条 + 多线程

处理大文件时，界面会卡死。需要把耗时操作放到子线程，用信号更新进度条：

```python
from PyQt5.QtCore import QThread, pyqtSignal

class Worker(QThread):
    progress = pyqtSignal(int)  # 发送进度 0-100

    def run(self):
        for i, item in enumerate(data):
            process(item)
            self.progress.emit(int((i+1) / len(data) * 100))

# 主线程里
self.worker = Worker()
self.worker.progress.connect(self.progress_bar.setValue)
self.worker.start()
```

## 踩坑记录

- **不能在子线程里直接操作 UI**，必须通过信号传回主线程
- `exec_()` 在 PyQt5 里已弃用，改用 `exec()`（新版本）
- 打包成 exe 用 PyInstaller，但图片/图标需要用 `sys._MEIPASS` 处理路径问题

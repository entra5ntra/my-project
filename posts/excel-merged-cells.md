---
date: 2026-01-15
tag: 踩坑
title: Excel 合并单元格处理方案汇总
---

## 问题描述

用 openpyxl 读取有合并单元格的 Excel 时，只有合并区域左上角的格子有值，其他位置读出来都是 `None`。

```python
# 比如 A1:A3 是合并单元格，值是"苹果"
ws['A1'].value  # "苹果"
ws['A2'].value  # None  ← 坑就在这
ws['A3'].value  # None
```

## 方案一：读前先取消合并

```python
# 复制合并区域信息，取消合并，然后填充值
merges = list(ws.merged_cells.ranges)
for merged_range in merges:
    top_left_value = ws.cell(merged_range.min_row, merged_range.min_col).value
    ws.unmerge_cells(str(merged_range))
    for row in ws.iter_rows(
        min_row=merged_range.min_row, max_row=merged_range.max_row,
        min_col=merged_range.min_col, max_col=merged_range.max_col
    ):
        for cell in row:
            cell.value = top_left_value
```

**优点**：之后可以正常用索引访问
**缺点**：修改了原始数据，如果需要保留合并格式就不行

## 方案二：读时向上查找

不修改原数据，读值时如果是 `None` 就往上找：

```python
def get_cell_value(ws, row, col):
    value = ws.cell(row, col).value
    if value is not None:
        return value
    # 检查是否在合并区域内
    for merged in ws.merged_cells.ranges:
        if (merged.min_row <= row <= merged.max_row and
                merged.min_col <= col <= merged.max_col):
            return ws.cell(merged.min_row, merged.min_col).value
    return None
```

## 方案三：用 pandas

如果不在意格式，直接 pandas 读，它会自动 `ffill` 填充合并单元格：

```python
import pandas as pd
df = pd.read_excel('file.xlsx', header=0)
df = df.fillna(method='ffill')  # 向前填充
```

## 我的选择

处理供应商文件时用**方案一**，因为后续要大量按行列取值，直接操作最方便。

考勤报表用**方案三**，数据量大，pandas 更快。

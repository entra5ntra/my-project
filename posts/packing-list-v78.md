---
date: 2026-02-10
tag: 工具开发
title: 出货单处理系统 v7.8 开发总结
---

## 背景

这个工具的核心需求是：把供应商发来的各种格式的交货文件，统一转换成公司内部标准的 SKU 编码格式。

## 主要改进

v7.8 相比之前的版本主要解决了以下问题：

- 复合型号的拆分识别（如 `A123/B456` 需要分开处理）
- 数据格式变体的兼容（同一个型号有多种写法）
- GUI 操作流程优化

## 核心算法

三级匹配策略：

1. **精确匹配** — 直接查字典，命中率约 60%
2. **规则化匹配** — 去掉空格/特殊字符后再匹配，覆盖约 30%
3. **模糊匹配** — 用 FuzzyWuzzy 兜底，处理剩余 10%

```python
def match_sku(raw_code, sku_dict):
    # 精确匹配
    if raw_code in sku_dict:
        return sku_dict[raw_code], 'exact'

    # 规则化匹配
    normalized = normalize(raw_code)
    if normalized in sku_dict:
        return sku_dict[normalized], 'rule'

    # 模糊匹配
    result, score = process.extractOne(normalized, sku_dict.keys())
    if score >= 85:
        return sku_dict[result], 'fuzzy'

    return None, 'unmatched'
```

## 踩过的坑

**合并单元格处理**：openpyxl 读取合并单元格时，只有左上角的格子有值，其余都是 `None`。需要先 `unmerge_cells` 或者手动填充。

**编码问题**：供应商发来的文件有时是 GBK 编码，直接 `read_text()` 会报错。统一用 `chardet` 检测编码再处理。

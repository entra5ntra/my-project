#!/usr/bin/env python3
"""
build.py - 文章构建脚本
将 posts/*.md 转换为 HTML 页面，并更新 articles.js

用法: python build.py
依赖: pip install markdown
"""

import re
from pathlib import Path

try:
    import markdown
except ImportError:
    print("错误: 请先安装 markdown 库")
    print("      pip install markdown")
    exit(1)

BASE_DIR = Path(__file__).parent
POSTS_DIR = BASE_DIR / "posts"
OUTPUT_JS = BASE_DIR / "articles.js"

# ──────────────────────────────────────────
# 文章页面 HTML 模板
# 占位符: %%TITLE%% %%DATE%% %%TAG%% %%BODY%%
# ──────────────────────────────────────────
TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>%%TITLE%% · ENTRA</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;900&family=Noto+Sans+SC:wght@300;400;500;700;900&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root {
  --bg: #080c18;
  --text1: #e8ecf4;
  --text2: #7a92b5;
  --accent: #5eafed;
  --glass-card: rgba(255,255,255,0.06);
  --glass-card-border: rgba(255,255,255,0.1);
  --R: 16px;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: var(--bg); color: var(--text1); font-family: 'Noto Sans SC', sans-serif; min-height: 100vh; padding: 48px 20px; }
.wrap { max-width: 720px; margin: 0 auto; }
.back { display: inline-flex; align-items: center; gap: 6px; color: var(--text2); text-decoration: none; font-size: 14px; font-family: 'JetBrains Mono', monospace; margin-bottom: 48px; transition: color .2s; }
.back:hover { color: var(--accent); }
.meta { display: flex; align-items: center; gap: 12px; margin-bottom: 20px; }
.meta-date { font-family: 'JetBrains Mono', monospace; font-size: 13px; color: var(--text2); }
.meta-tag { font-size: 11px; font-weight: 500; padding: 4px 12px; border-radius: 6px; background: var(--glass-card); color: var(--accent); border: 1px solid var(--glass-card-border); }
h1 { font-size: 28px; font-weight: 700; line-height: 1.4; margin-bottom: 36px; }
.content { line-height: 1.9; font-size: 16px; font-weight: 300; }
.content h2 { font-size: 20px; font-weight: 600; margin: 40px 0 16px; }
.content h3 { font-size: 17px; font-weight: 600; margin: 32px 0 12px; }
.content p { margin-bottom: 18px; }
.content ul, .content ol { margin: 0 0 18px 24px; }
.content li { margin-bottom: 8px; }
.content code { font-family: 'JetBrains Mono', monospace; font-size: 13px; background: rgba(94,175,237,0.12); padding: 2px 6px; border-radius: 4px; color: var(--accent); }
.content pre { background: rgba(13,26,52,0.85); border: 1px solid var(--glass-card-border); border-radius: var(--R); padding: 20px; overflow-x: auto; margin-bottom: 18px; }
.content pre code { background: none; padding: 0; color: var(--text1); font-size: 14px; }
.content blockquote { border-left: 3px solid var(--accent); padding-left: 16px; margin: 0 0 18px; color: var(--text2); }
.content a { color: var(--accent); text-decoration: none; }
.content a:hover { text-decoration: underline; }
.content hr { border: none; border-top: 1px solid var(--glass-card-border); margin: 32px 0; }
.content table { width: 100%; border-collapse: collapse; margin-bottom: 18px; font-size: 14px; }
.content th, .content td { border: 1px solid var(--glass-card-border); padding: 10px 14px; text-align: left; }
.content th { background: var(--glass-card); color: var(--accent); }
</style>
</head>
<body>
<div class="wrap">
  <a class="back" href="../index.html">← 返回首页</a>
  <div class="meta">
    <span class="meta-date">%%DATE%%</span>
    <span class="meta-tag">%%TAG%%</span>
  </div>
  <h1>%%TITLE%%</h1>
  <div class="content">
%%BODY%%
  </div>
</div>
</body>
</html>"""


def parse_frontmatter(text):
    """解析 --- 包裹的 YAML 头部，返回 (meta dict, body str)"""
    m = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)', text, re.DOTALL)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).splitlines():
        if ':' in line:
            k, _, v = line.partition(':')
            meta[k.strip()] = v.strip()
    return meta, m.group(2)


def build():
    POSTS_DIR.mkdir(exist_ok=True)
    md_files = sorted(POSTS_DIR.glob("*.md"))

    if not md_files:
        print("posts/ 里没有 .md 文件，请先创建文章。")
        print("格式参考: posts/ 目录下任意 .md 文件")
        return

    articles = []

    for md_path in md_files:
        text = md_path.read_text(encoding='utf-8')
        meta, body = parse_frontmatter(text)

        date  = meta.get('date',  '未知日期')
        tag   = meta.get('tag',   '随笔')
        title = meta.get('title', md_path.stem)

        body_html = markdown.markdown(
            body.strip(),
            extensions=['fenced_code', 'tables']
        )

        html = (TEMPLATE
                .replace('%%TITLE%%', title)
                .replace('%%DATE%%',  date)
                .replace('%%TAG%%',   tag)
                .replace('%%BODY%%',  body_html))

        out_path = POSTS_DIR / (md_path.stem + '.html')
        out_path.write_text(html, encoding='utf-8')
        print(f"  生成: posts/{md_path.stem}.html  [{tag}] {title}")

        articles.append({
            'date':  date,
            'tag':   tag,
            'title': title,
            'url':   f'posts/{md_path.stem}.html',
        })

    # 按日期倒序
    articles.sort(key=lambda a: a['date'], reverse=True)

    # 写出 articles.js
    lines = [
        '// 此文件由 build.py 自动生成，请勿手动修改',
        '// 修改文章后运行: python build.py',
        'const ARTICLES = [',
    ]
    for a in articles:
        lines.append(
            f'  {{ date: "{a["date"]}", tag: "{a["tag"]}", '
            f'title: "{a["title"]}", url: "{a["url"]}" }},'
        )
    lines.append('];')
    OUTPUT_JS.write_text('\n'.join(lines) + '\n', encoding='utf-8')

    print(f"\narticles.js 已更新，共 {len(articles)} 篇文章。")
    print("刷新浏览器即可看到最新列表。")


if __name__ == '__main__':
    build()

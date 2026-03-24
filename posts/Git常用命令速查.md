> 基于实际使用场景整理，适合入门参考

---

## 一、首次使用：初始化 + 推送到 GitHub

```bash
# 1. 进入项目文件夹（不要在桌面根目录操作！）
cd C:/Users/你的用户名/Desktop/my-project

# 2. 初始化 git 仓库（只需执行一次）
git init

# 3. 把所有文件加入暂存区
git add .

# 4. 提交（相当于"存档"）
git commit -m "first commit"

# 5. 关联远程 GitHub 仓库（只需一次）
git remote add origin https://github.com/你的用户名/仓库名.git

# 6. 设置主分支名为 main
git branch -M main

# 7. 推送到 GitHub
git push -u origin main
```

**注意：** `git add .` 会添加当前目录下所有文件，所以一定要先 `cd` 到项目文件夹里，不要在桌面执行。

---

## 二、日常更新：改了代码推上去

每次修改代码后，只需要三条命令：

```bash
git add .
git commit -m "描述你改了什么"
git push
```

例如：
```bash
git add .
git commit -m "修复导航栏标签闭合问题"
git push
```

---

## 三、查看状态

```bash
# 看哪些文件被修改了
git status

# 看提交历史
git log --oneline

# 查看当前关联的远程仓库地址
git remote -v
```

---

## 四、撤销和回退

```bash
# 撤销所有未提交的修改（回到上次 commit 的状态）
git checkout .

# 暂存当前修改（不想提交但也不想丢）
git stash

# 恢复暂存的修改
git stash pop
```

---

## 五、远程仓库相关

```bash
# 添加远程仓库（首次）
git remote add origin https://github.com/用户名/仓库名.git

# 修改远程仓库地址（换地址时用）
git remote set-url origin https://github.com/用户名/仓库名.git

# 强制推送（远程和本地冲突，确定要用本地覆盖远程时）
git push --force

# 拉取远程最新代码
git pull
```

---

## 六、配置相关

```bash
# 查看全局配置
git config --global --list

# 查看是否有 URL 替换规则（代理相关）
git config --global --list | findstr url

# 删除某条配置（比如删掉代理替换规则）
git config --global --unset url.https://某个代理地址/.insteadof

# 设置用户名和邮箱（首次使用 git 需要设置）
git config --global user.name "你的名字"
git config --global user.email "你的邮箱"
```

---

## 七、实用技巧

### 不想提交某些文件？

在项目根目录创建 `.gitignore` 文件：

```
# 忽略 node_modules
node_modules/

# 忽略 Python 缓存
__pycache__/
*.pyc

# 忽略系统文件
.DS_Store
Thumbs.db

# 忽略敏感配置
config.ini
.env
```

### GitHub Pages 部署流程

1. 代码推送到 GitHub
2. 仓库 Settings → Pages → Source 选 main 分支
3. 等 1-2 分钟，访问 `https://用户名.github.io/仓库名/`
4. 以后每次 `git push` 会自动重新部署

### 页面更新后看不到变化？

浏览器强制刷新：`Ctrl + Shift + R`

---

## 八、常见报错及解决

| 报错 | 原因 | 解决 |
|------|------|------|
| `nothing to commit, working tree clean` | 没有新的修改 | 正常，不用管 |
| `remote origin already exists` | 已经关联过远程仓库 | 用 `git remote set-url` 改地址 |
| `rejected (fetch first)` | 远程有本地没有的内容 | `git push --force`（确定要覆盖时） |
| `The requested URL returned error: 429` | 代理限流 | 检查并删除代理配置 |
| `unable to access` | 网络问题或地址错误 | 用 `git remote -v` 检查地址 |

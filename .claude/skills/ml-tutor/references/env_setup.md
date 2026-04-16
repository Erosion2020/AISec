# ml-tutor 环境配置指南

运行 `extract_pdf_pages.py` 时需要有可用的 Python 解释器和 pdfplumber。
本文档分两部分：**检测已有环境**（优先复用）和**创建新环境**（兜底）。
所有 pip 安装均使用清华镜像源。

**执行前提**：确定当前操作系统，按以下顺序判断：

1. 若 profile（`.claude/ml-learner-profile.md`）已存在 → 直接读取「基础配置」中的 `操作系统` 字段
2. 若 profile 尚未创建（首次运行）→ 根据 `pwd` 输出格式判断：
   - 路径以 `/` 开头（如 `/Users/...`、`/home/...`）→ macOS / Linux
   - 路径以盘符开头（如 `D:\...`）或 Git Bash 下为 `/d/...` → Windows

确定后，所有命令按对应平台执行，不需要在本文件内重新询问。

---

## 一、检测已有环境（按优先级）

按以下顺序检测，找到第一个可用的就停止，记为 `<PYTHON>`。

### 1. conda — ml-tutor 环境

```bash
conda env list 2>/dev/null | grep -q "ml-tutor"
```

存在时获取解释器绝对路径（**不要用 `conda run`**，Windows 上有编码 bug）：

```bash
conda info --base
```

按平台拼接路径：
- macOS/Linux：`<base>/envs/ml-tutor/bin/python`
- Windows：`<base>\envs\ml-tutor\python.exe`

不存在 → 继续下一步。

### 2. uv — ml-tutor 环境

```bash
uv --version 2>/dev/null
```

如果 uv 存在，按平台检查 ml-tutor 环境：

- macOS/Linux：`$HOME/.local/share/uv/envs/ml-tutor/bin/python`
- Windows：`%LOCALAPPDATA%\uv\envs\ml-tutor\Scripts\python.exe`

存在 → 使用该路径；不存在 → 继续下一步。

### 3. 工作目录内 venv

在工作目录下查找 `.venv`、`venv`、`env`：

- macOS/Linux：`<工作目录>/.venv/bin/python`（或 `venv/bin/python`、`env/bin/python`）
- Windows：`<工作目录>\.venv\Scripts\python.exe`（或 `venv\...`、`env\...`）

找到 → 使用该路径；未找到 → 进入下一节。

---

## 二、创建新环境（兜底策略）

按 conda → uv → python -m venv 顺序尝试，优先选有 ml-tutor 命名的独立环境。

### 方案 A：conda

```bash
# 创建环境（清华 conda 源）
conda create -n ml-tutor python=3.11 -y \
  -c https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main

# 获取解释器路径（见上方第1步的拼接规则）
conda info --base

# 安装依赖（用绝对路径的 pip）
# macOS/Linux：
"<base>/envs/ml-tutor/bin/pip" install pdfplumber \
  --index-url https://pypi.tuna.tsinghua.edu.cn/simple

# Windows：
"<base>\envs\ml-tutor\Scripts\pip.exe" install pdfplumber \
  --index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

### 方案 B：uv

```bash
# macOS/Linux：
uv venv ~/.local/share/uv/envs/ml-tutor --python 3.11
uv pip install pdfplumber \
  --python ~/.local/share/uv/envs/ml-tutor/bin/python \
  --index-url https://pypi.tuna.tsinghua.edu.cn/simple

# Windows：
uv venv "%LOCALAPPDATA%\uv\envs\ml-tutor" --python 3.11
uv pip install pdfplumber \
  --python "%LOCALAPPDATA%\uv\envs\ml-tutor\Scripts\python.exe" \
  --index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

### 方案 C：python -m venv（最终兜底）

```bash
# macOS/Linux：
python -m venv ~/.local/share/ml-tutor-venv
~/.local/share/ml-tutor-venv/bin/pip install pdfplumber \
  --index-url https://pypi.tuna.tsinghua.edu.cn/simple

# Windows：
python -m venv "%LOCALAPPDATA%\ml-tutor-venv"
"%LOCALAPPDATA%\ml-tutor-venv\Scripts\pip" install pdfplumber \
  --index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

---

## 三、所有方案都不可用

告知用户：

> 我在你的系统上没有检测到 conda、uv 或 python，无法自动配置环境。
> 推荐安装 Miniconda 或 uv：
> - Miniconda：https://docs.conda.io/en/latest/miniconda.html
> - uv：https://docs.astral.sh/uv/getting-started/installation/
>
> 或者直接把想理解的段落复制过来，我帮你解释。


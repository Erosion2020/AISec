# ml-tutor 环境配置指南

运行 `extract_pdf_pages.py` 时需要有可用的 Python 解释器和依赖包。
本文档分两部分：**检测已有环境**（主动查找，优先复用）和**创建新环境**（兜底创建）。
所有 pip 安装均使用清华镜像源。

---

## 一、检测已有环境（优先级顺序）

按以下顺序检测，找到第一个可用的就停止，记为 `<PYTHON>`。

### 1. conda — ml-tutor 环境

```bash
conda env list 2>/dev/null | grep -q "ml-tutor"
```

- **存在** → 获取解释器绝对路径（**不要用 `conda run`**，Windows 上存在编码 bug）：
  ```bash
  # 获取 conda base 目录
  conda info --base
  # Windows 解释器路径：<base>\envs\ml-tutor\python.exe
  # Linux / macOS 解释器路径：<base>/envs/ml-tutor/bin/python
  ```
  Windows 上运行脚本时加 `PYTHONUTF8=1` 前缀，避免控制台编码问题：
  ```bash
  # Windows（在 bash/Git Bash 中）
  PYTHONUTF8=1 "<base>\envs\ml-tutor\python.exe" scripts/extract_pdf_pages.py ...
  # Linux / macOS
  "<base>/envs/ml-tutor/bin/python" scripts/extract_pdf_pages.py ...
  ```
- **conda 未安装 / 环境不存在** → 继续下一步

### 2. uv — ml-tutor 环境

先检查 uv 是否存在：

```bash
uv --version 2>/dev/null
```

如果 uv 存在，检查 ml-tutor 环境：

```bash
# Windows
test -f "%LOCALAPPDATA%\uv\envs\ml-tutor\Scripts\python.exe"

# Linux / macOS
test -f "$HOME/.local/share/uv/envs/ml-tutor/bin/python"
```

- **存在** → 使用对应路径的 python 解释器
- **uv 未安装 / 环境不存在** → 继续下一步

### 3. 项目内 venv

在当前项目根目录查找标准 venv 目录（`.venv`、`venv`、`env`）：

```bash
# Windows — 依次检查
.venv\Scripts\python.exe
venv\Scripts\python.exe
env\Scripts\python.exe

# Linux / macOS — 依次检查
.venv/bin/python
venv/bin/python
env/bin/python
```

- **找到** → 使用该路径的 python 解释器
- **未找到** → 进入下一节"创建新环境"

---

## 二、创建新环境（兜底策略）

没有找到可用环境时，按 conda → uv → python -m venv 顺序尝试创建。

### 方案 A：conda（优先）

```bash
# 1. 创建 ml-tutor 环境（使用清华 conda 源）
conda create -n ml-tutor python=3.11 -y \
  -c https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main

# 2. 获取解释器绝对路径（避免 conda run 在 Windows 上的编码 bug）
conda info --base
# 输出示例（Windows）：C:\Users\yourname\.conda
# 输出示例（Linux/macOS）：/home/yourname/miniconda3

# 根据上面的输出拼接路径：
# Windows：
#   解释器：<base>\envs\ml-tutor\python.exe
#   pip：   <base>\envs\ml-tutor\Scripts\pip.exe
# Linux / macOS：
#   解释器：<base>/envs/ml-tutor/bin/python
#   pip：   <base>/envs/ml-tutor/bin/pip

# 3. 安装核心依赖（用绝对路径的 pip，清华 PyPI 源）
# Windows（将 <base> 替换为实际路径）：
"<base>\envs\ml-tutor\Scripts\pip.exe" install pdfplumber \
  --index-url https://pypi.tuna.tsinghua.edu.cn/simple
# Linux / macOS：
# <base>/envs/ml-tutor/bin/pip install pdfplumber \
#   --index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 4. 可选：安装 OCR 支持（失败不影响基础功能）
# Windows：
"<base>\envs\ml-tutor\Scripts\pip.exe" install pdf2image pytesseract \
  --index-url https://pypi.tuna.tsinghua.edu.cn/simple
# Linux / macOS：
# <base>/envs/ml-tutor/bin/pip install pdf2image pytesseract \
#   --index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 创建完成后，使用绝对路径调用解释器（不要用 conda run）：
# Windows：  "<base>\envs\ml-tutor\python.exe" script.py
# Linux/mac：<base>/envs/ml-tutor/bin/python script.py
```

### 方案 B：uv

```bash
# 1. 创建虚拟环境（uv 会自动下载所需 Python）
#    Linux / macOS：
uv venv ~/.local/share/uv/envs/ml-tutor --python 3.11
#    Windows：
#    uv venv "%LOCALAPPDATA%\uv\envs\ml-tutor" --python 3.11

# 2. 安装核心依赖（清华 PyPI 源）
#    Linux / macOS：
uv pip install pdfplumber \
  --python ~/.local/share/uv/envs/ml-tutor/bin/python \
  --index-url https://pypi.tuna.tsinghua.edu.cn/simple
#    Windows：
#    uv pip install pdfplumber \
#      --python "%LOCALAPPDATA%\uv\envs\ml-tutor\Scripts\python.exe" \
#      --index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 3. 可选：安装 OCR 支持
#    Linux / macOS：
uv pip install pdf2image pytesseract \
  --python ~/.local/share/uv/envs/ml-tutor/bin/python \
  --index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 创建完成后，使用对应路径的 python 解释器运行脚本
```

### 方案 C：python -m venv（最终兜底）

```bash
# 1. 创建 venv
#    Linux / macOS：
python -m venv ~/.local/share/ml-tutor-venv
#    Windows：
#    python -m venv "%LOCALAPPDATA%\ml-tutor-venv"

# 2. 安装核心依赖（清华 PyPI 源）
#    Linux / macOS：
~/.local/share/ml-tutor-venv/bin/pip install pdfplumber \
  --index-url https://pypi.tuna.tsinghua.edu.cn/simple
#    Windows：
#    "%LOCALAPPDATA%\ml-tutor-venv\Scripts\pip" install pdfplumber \
#      --index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 3. 可选：安装 OCR 支持
#    Linux / macOS：
~/.local/share/ml-tutor-venv/bin/pip install pdf2image pytesseract \
  --index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 创建完成后，使用 ~/.local/share/ml-tutor-venv/bin/python
# Windows："%LOCALAPPDATA%\ml-tutor-venv\Scripts\python.exe"
```

---

## 三、所有方案都不可用

如果 conda、uv、python 均未安装，告知用户：

> 我在你的系统上没有检测到 conda、uv 或 python，无法自动配置环境。
> 推荐安装 conda（Miniconda）或 uv，然后再试：
> - Miniconda：https://docs.conda.io/en/latest/miniconda.html
> - uv：https://docs.astral.sh/uv/getting-started/installation/
>
> 或者直接把想理解的那段文字复制过来，我帮你解释。

---

## 四、OCR 依赖说明

`pdf2image` 和 `pytesseract` 是可选的，只在遇到图片型 PDF 页时才需要。
除了 pip 包，还需要系统级安装 Tesseract-OCR：

- Windows：https://github.com/UB-Mannheim/tesseract/wiki
- macOS：`brew install tesseract tesseract-lang`
- Linux：`sudo apt install tesseract-ocr tesseract-ocr-chi-sim`

OCR 安装失败不影响纯文字 PDF 的提取。

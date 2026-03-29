# ml-tutor 环境配置指南

当运行 `extract_pdf_pages.py` 失败（找不到 python、缺少依赖等）时，查阅本文档。
根据用户系统上可用的工具，选择对应方案。所有 pip 安装均使用清华镜像源。

---

## 检测可用工具

依次检测以下命令是否存在，按 conda → uv → pip 优先级选择方案：

```bash
conda --version
uv --version
pip --version   # 或 pip3 --version
```

---

## 方案 A：conda（优先）

适用：系统有 conda（Anaconda / Miniconda），但可能没有全局 python。

```bash
# 1. 创建 ml-tutor 环境，指定 Python 版本，使用清华 conda 源
conda create -n ml-tutor python=3.11 -y -c https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main

# 2. 找到该环境的 python 解释器路径（不用激活环境）
#    Linux / macOS：
conda run -n ml-tutor which python
#    Windows：
conda run -n ml-tutor where python

# 3. 用该解释器安装依赖（清华 PyPI 源）
conda run -n ml-tutor pip install pdfplumber --index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 4. 可选：安装 OCR 支持（失败不影响基础功能）
conda run -n ml-tutor pip install pdf2image pytesseract --index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 5. 用环境内的 python 运行提取脚本
conda run -n ml-tutor python scripts/extract_pdf_pages.py "<pdf路径>" <起始页> <结束页>
```

**注意**：`conda run -n ml-tutor python ...` 无需激活环境，直接用指定环境的解释器执行，适合脚本调用。

如果环境已存在，跳过第 1 步，直接从第 5 步执行。检测是否已存在：

```bash
conda env list | grep ml-tutor
```

---

## 方案 B：uv

适用：系统有 uv，没有 conda。

```bash
# 1. 创建虚拟环境（uv 会自动下载所需 Python 版本）
uv venv ~/.local/share/uv/envs/ml-tutor --python 3.11

# 2. 安装依赖（清华源）
uv pip install pdfplumber \
  --python ~/.local/share/uv/envs/ml-tutor/bin/python \
  --index-url https://pypi.tuna.tsinghua.edu.cn/simple

# Windows 路径示例：
# uv pip install pdfplumber \
#   --python %LOCALAPPDATA%\uv\envs\ml-tutor\Scripts\python.exe \
#   --index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 3. 可选：安装 OCR 支持
uv pip install pdf2image pytesseract \
  --python ~/.local/share/uv/envs/ml-tutor/bin/python \
  --index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 4. 运行提取脚本
~/.local/share/uv/envs/ml-tutor/bin/python scripts/extract_pdf_pages.py "<pdf路径>" <起始页> <结束页>
# Windows：
# %LOCALAPPDATA%\uv\envs\ml-tutor\Scripts\python.exe scripts/extract_pdf_pages.py "<pdf路径>" <起始页> <结束页>
```

如果环境已存在，跳过第 1~3 步，直接运行第 4 步。

---

## 方案 C：pip / venv

适用：系统有 pip/pip3 和 python，没有 conda 和 uv。

```bash
# 1. 创建 venv
python -m venv ~/.local/share/ml-tutor-venv
# Windows：
# python -m venv %LOCALAPPDATA%\ml-tutor-venv

# 2. 安装依赖（清华源）
~/.local/share/ml-tutor-venv/bin/pip install pdfplumber --index-url https://pypi.tuna.tsinghua.edu.cn/simple
# Windows：
# %LOCALAPPDATA%\ml-tutor-venv\Scripts\pip install pdfplumber --index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 3. 可选：安装 OCR 支持
~/.local/share/ml-tutor-venv/bin/pip install pdf2image pytesseract --index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 4. 运行提取脚本
~/.local/share/ml-tutor-venv/bin/python scripts/extract_pdf_pages.py "<pdf路径>" <起始页> <结束页>
# Windows：
# %LOCALAPPDATA%\ml-tutor-venv\Scripts\python.exe scripts/extract_pdf_pages.py "<pdf路径>" <起始页> <结束页>
```

---

## 所有方案都不可用

如果 conda、uv、pip 均未安装，告知用户：

> 我在你的系统上没有检测到 conda、uv 或 pip，无法自动配置环境。
> 推荐安装 conda（Miniconda）或 uv，然后再试：
> - Miniconda：https://docs.conda.io/en/latest/miniconda.html
> - uv：https://docs.astral.sh/uv/getting-started/installation/
>
> 或者直接把想理解的那段文字复制过来，我帮你解释。

---

## OCR 依赖说明

`pdf2image` 和 `pytesseract` 是可选的，只在遇到图片型 PDF 页时才需要。
除了 pip 包，还需要系统级安装 Tesseract-OCR：

- Windows：https://github.com/UB-Mannheim/tesseract/wiki
- macOS：`brew install tesseract tesseract-lang`
- Linux：`sudo apt install tesseract-ocr tesseract-ocr-chi-sim`

OCR 安装失败不影响纯文字 PDF 的提取。

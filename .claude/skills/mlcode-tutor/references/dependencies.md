# ML 生态依赖兼容性参考

在为 Python ML 项目生成依赖文件时，需要检查以下已知的版本约束和冲突规则。

---

## 包管理工具选择（优先级：conda > uv > pip）

生成依赖文件时，按以下顺序检测并使用用户系统中可用的工具：

### 1. conda（首选）

**为什么 ML 项目首选 conda：**
- 能管理 Python 本身 + 系统级二进制依赖（CUDA toolkit、cudnn、MKL 等）
- ML 生态中大部分包在 conda-forge 上有预编译版本，安装失败率远低于 pip
- `environment.yml` 同时管理 pip 和 conda 依赖，兼容性好

**检测方式：**
- 执行 `conda list --json 2>/dev/null` 看是否返回 JSON
- 或者检查环境变量 `CONDA_DEFAULT_ENV` 是否有值
- 用户可能用的是 miniconda / anaconda / mamba（都兼容）

**生成文件**：`environment.yml`

```yaml
name: ml-env
channels:
  - pytorch        # PyTorch 官方 channel，提供 CUDA 版本
  - conda-forge    # 社区维护的大量预编译包
  - defaults
dependencies:
  - python=3.10
  - pytorch>=2.0          # conda 自动匹配 CUDA 版本
  - torchvision>=0.15     # conda 自动与 pytorch 版本对齐
  - numpy>=1.21,<2.0
  - pandas>=1.3
  - scikit-learn>=1.0
  - tqdm>=4.60
  - tensorboard>=2.12
  - pip                    # 用于 conda 没有的包
  - pip:
    - torchviz             # conda 没有的包通过 pip 安装
```

**安装命令**：`conda env create -f environment.yml`

### 2. uv（次选）

**为什么用 uv：**
- Rust 实现，比 pip 快 10-100 倍
- 有真正的依赖解析器和锁文件（`uv.lock`），比 `requirements.txt` 可靠
- 原生支持 `pyproject.toml`，是 Python 生态的未来方向

**检测方式：**
- 执行 `uv --version 2>/dev/null` 查看是否能运行
- 或者执行 `pip show uv` 查看是否安装

**生成文件**：`pyproject.toml`（或 `uv pip compile` 生成精确锁文件）

```toml
[project]
name = "ml-project"
requires-python = ">=3.10"
dependencies = [
    "torch>=2.0",
    "torchvision>=0.15",
    "numpy>=1.21,<2.0",
    "pandas>=1.3",
    "scikit-learn>=1.0",
    "tqdm>=4.60",
    "tensorboard>=2.12",
    "torchviz",
]

[tool.uv.sources]
# PyTorch 需要从官方 index 安装才能获得 CUDA 版本
torch = { index = "pytorch-cu121" }
torchvision = { index = "pytorch-cu121" }

[[tool.uv.index]]
name = "pytorch-cu121"
url = "https://download.pytorch.org/whl/cu121"
explicit = true
```

**安装命令**：
```bash
uv pip install -r <(uv pip compile pyproject.toml -o -)   # 从 pyproject.toml 解析
# 或直接用 uv sync
uv sync
```

### 3. pip + requirements.txt（回退）

只在 conda 和 uv 都不可用时使用。`requirements.txt` 有以下局限：
- 没有真正的依赖解析器（npm/maven 那种），冲突靠人工发现
- 不区分直接依赖和间接依赖
- `--index-url` 不能写在文件里，PyTorch 的 CUDA 版本需要单独说明

---

## PyTorch 生态的核心约束

### torch ↔ torchvision ↔ torchaudio 版本绑定

这三者的版本号**不是独立的**，PyTorch 官方维护了一个严格的版本对应表：

| torch | torchvision | torchaudio | Python 要求 |
|-------|-------------|------------|-------------|
| 2.5.x | 0.20.x | 2.5.x | >=3.9 |
| 2.4.x | 0.19.x | 2.4.x | >=3.8 |
| 2.3.x | 0.18.x | 2.3.x | >=3.8 |
| 2.2.x | 0.17.x | 2.2.x | >=3.8 |
| 2.1.x | 0.16.x | 2.1.x | >=3.8 |
| 2.0.x | 0.15.x | 2.0.x | >=3.8 |
| 1.13.x | 0.14.x | 0.13.x | >=3.7 |

**操作规则**：如果代码中同时 import 了 `torch` 和 `torchvision`，必须确保它们属于同一行（主版本对齐）。

### conda 用户安装 PyTorch 的优势

conda 安装 PyTorch 时自动选择与系统 CUDA 驱动匹配的版本：

```bash
# conda 会自动匹配 CUDA 版本
conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia
```

### pip/uv 安装 PyTorch 需要手动指定 CUDA 版本

| CUDA 版本 | pip index URL | 说明 |
|-----------|---------------|------|
| CUDA 12.4 | `https://download.pytorch.org/whl/cu124` | PyTorch 2.5 默认 |
| CUDA 12.1 | `https://download.pytorch.org/whl/cu121` | PyTorch 2.2-2.4 默认 |
| CUDA 11.8 | `https://download.pytorch.org/whl/cu118` | 老显卡兼容 |
| CPU only | `https://download.pytorch.org/whl/cpu` | 无 GPU 或 macOS |

**操作规则**：
- 如果代码中有 `device = 'cuda' if torch.cuda.is_available() else 'cpu'`，优先推荐 CUDA 版本
- 如果操作系统是 macOS 或没有 NVIDIA GPU，用 CPU 版本
- 对于 pip/requirements.txt：不要在文件中写 `--index-url`（pip 不支持），在注释中给出安装命令
- 对于 uv：可以在 `pyproject.toml` 中用 `[[tool.uv.index]]` 配置 PyTorch 源

### torchviz 的特殊性

```python
from torchviz import make_dot  # import 名是 torchviz
# pip install torchviz         # pip 包名也叫 torchviz
```
- `torchviz` 依赖 `graphviz`（不是 Python 包，是系统级工具）
  - Ubuntu: `apt install graphviz`
  - macOS: `brew install graphviz`
  - Windows: 需要下载安装 Graphviz 并添加到 PATH
- 在 `requirements.txt` 中只写 `torchviz`，但在注释中提醒系统级依赖

---

## NumPy ↔ 其他库的兼容性

### 常见冲突

| NumPy 版本 | 风险 |
|-----------|------|
| numpy >= 1.25 | 部分旧版 sklearn (<1.2) 可能报 deprecation warning（一般不阻断） |
| numpy >= 2.0 | **重大 API 变更**，大量 ML 库还没适配（2024-2025 年过渡期），谨慎使用 |
| numpy < 1.20 | 缺少 `numpy.typing` 等较新的类型提示，新版 torch 可能不兼容 |

**操作规则**：
- 默认推荐 `numpy>=1.21,<2.0`（保守安全范围）
- 如果代码中用了 `numpy>=2.0` 的新 API（如 `numpy.array_api`），才放开上限
- 排查时优先看项目中的 `sklearn` 版本要求

### Pandas ↔ NumPy

Pandas 版本与 NumPy 版本一般没有硬冲突，但：
- `pandas>=2.0` 需要 `numpy>=1.20`
- 如果代码中用了 `pd.set_option('display.max_column', ...)`（已废弃，新 API 是 `pd.set_option('display.max_columns', ...)`），说明用户用的是较老版本

---

## sklearn (scikit-learn) 兼容性

### 包名陷阱

```python
from sklearn.model_selection import train_test_split  # import 名是 sklearn
# pip install scikit-learn                              # pip 包名是 scikit-learn！
```

这是新手最容易搞错的地方——Python 包名和 pip 包名不一致。**生成 requirements.txt 时一定要写 `scikit-learn`，不是 `sklearn`。**

### 版本约束

| sklearn 版本 | Python 要求 | 关键变化 |
|-------------|------------|---------|
| 1.5.x | >=3.9 | 当前最新 |
| 1.3.x-1.4.x | >=3.8 | 较稳定 |
| 1.0.x-1.2.x | >=3.7 | 广泛兼容 |

---

## TensorBoard

```python
from torch.utils.tensorboard import SummaryWriter
# pip install tensorboard
```
- `torch.utils.tensorboard` 实际上是 TensorBoard 的 PyTorch 封装，底层依赖 `tensorboard` 包
- `tensorboard` 一般与 `torch` 版本解耦，使用最新稳定版即可
- 如果代码还用了 `TensorBoardX`（老项目常见），则 `tensorboardX` 和 `tensorboard` 是两个不同的包

---

## 其他常见包名映射

| import 名 | pip 包名 | 备注 |
|-----------|----------|------|
| `sklearn` | `scikit-learn` | 最常见的搞错 |
| `cv2` | `opencv-python` (或 `opencv-python-headless`) | 服务器用 headless 版 |
| `PIL` | `Pillow` | |
| `yaml` | `PyYAML` | 注意大小写 |
| `bs4` / `BeautifulSoup` | `beautifulsoup4` | |
| `tqdm` | `tqdm` | 一致 |
| `matplotlib` | `matplotlib` | 一致 |

---

## 操作系统特定处理

### Windows

- `pycocotools` 在 Windows 上编译安装经常失败 → 推荐 `pycocotools-windows`
- 文件路径使用反斜杠 → 检查代码中是否有硬编码路径，提醒用户用 `pathlib` 或 `/`
- `num_workers > 0` 在 Windows 上需要 `if __name__ == '__main__':` 保护（否则 DataLoader 会 fork 失败）

### macOS (Apple Silicon / M1 M2 M3)

- PyTorch 在 Apple Silicon 上默认使用 MPS 加速（`mps` device），**不需要 CUDA**
- pip 安装命令：`pip install torch torchvision torchaudio`
- 部分操作不支持 MPS（如某些 RNN 算子），代码中应该有 fallback 到 CPU 的逻辑

### Linux

- CUDA 版本的 PyTorch 需要匹配 NVIDIA 驱动版本
- 检查 `nvidia-smi` 输出可以确定支持的 CUDA 版本上限
- `num_workers > 0` 在 Linux 上通常没有 fork 问题

---

## 生成模板汇总

根据检测到的工具选择对应模板：

### conda → environment.yml
```yaml
name: ml-env
channels:
  - pytorch
  - conda-forge
  - defaults
dependencies:
  - python=3.10
  - pytorch>=2.0
  - torchvision>=0.15  # 必须与 torch 主版本一致
  - numpy>=1.21,<2.0
  - pandas>=1.3
  - scikit-learn>=1.0
  - tqdm>=4.60
  - tensorboard>=2.12
  - pip
  - pip:
    - torchviz  # conda 没有的包通过 pip 补充
```

### uv → pyproject.toml
```toml
[project]
name = "ml-project"
requires-python = ">=3.10"
dependencies = [
    "torch>=2.0",
    "torchvision>=0.15",
    "numpy>=1.21,<2.0",
    "pandas>=1.3",
    "scikit-learn>=1.0",
    "tqdm>=4.60",
    "tensorboard>=2.12",
    "torchviz",
]
```

### pip → requirements.txt（仅作 fallback）
```
# 深度学习框架
# 安装命令 (CUDA 12.1): pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
torch>=2.0
torchvision>=0.15  # 必须与 torch 主版本一致

# 数据处理
numpy>=1.21,<2.0
pandas>=1.3
scikit-learn>=1.0

# 工具
tqdm>=4.60
tensorboard>=2.12

# 可视化 (可选)
# torchviz 还需要系统安装 graphviz
torchviz
```

---

## 依赖冲突排查流程

当用户代码同时依赖了 A 和 B 时，按以下顺序检查：

1. **查官方文档**：A 和 B 是否有明确的版本对应关系？（如 torch ↔ torchvision）
2. **查 NumPy**：这是最常见的冲突源——A 要求 `numpy>=X`，B 要求 `numpy<X`
3. **查 Python 版本**：有没有哪个包放弃了对当前 Python 版本的支持？
4. **搜索已知问题**：在包的 GitHub Issues 中搜索 "A + B version conflict"

如果找到冲突：
- 优先选择**兼容范围更宽**的那个版本约束
- 如果无法调和，**明确告知用户**，列出两条路径让用户选择：
  - 降级 A → 版本 X
  - 降级 B → 版本 Y

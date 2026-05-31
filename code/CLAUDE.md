# code/ 目录指南（AI Agent 自动加载）

## 目录结构

```
code/
  work1/     # COVID-19 阳性率预测（回归模型）
  work2/     # 未来扩展...
```

每个子目录有独立的 `environment.yml`，互不冲突。

---

## work1 — COVID-19 阳性率预测

### 数据集

| 数据集 | 描述 | 下载 |
|---|---|---|
| `covid.train.csv` | 2699 条 × 118 列（117 特征 + 标签） | [Google Drive](https://drive.google.com/uc?id=1kLSW_-cW2Huj7bh84YTdimGBOJaODiOS) |
| `covid.test.csv` | 1078 条 × 117 列（仅特征，无标签） | [Google Drive](https://drive.google.com/uc?id=1iiI5qROrAhZn-o4FPqsE97bMzDEFvIdg) |

代码期望文件名为 `covid.train.csv` 和 `covid.test.csv`，下载后若文件名不同需重命名。

### 模型简介

三层 MLP（117→16→8→1），输入过去 5 天疫情特征 → 输出当天阳性率预测值。

---

## 环境创建与激活

### 通用规则

1. **每个子目录的环境独立**，用各自目录下的 `environment.yml` 创建
2. **工具优先级**：conda > uv > pip（conda 能一并管理 CUDA toolkit）
3. **安装源**：中国大陆用户优先用清华源，非大陆用户用默认源
4. **创建命令**：
   ```bash
   # 大陆用户
   conda env create -f environment.yml -c https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge
   # 非大陆用户
   conda env create -f environment.yml
   ```

### 平台差异

| 平台 | 特殊处理 |
|---|---|
| **Windows** | CUDA pytorch 需要手动加 `pytorch-cuda=12.4`（见下方坑点） |
| **macOS (Apple Silicon)** | 不用 CUDA，pytorch 默认走 MPS。删除 `pytorch-cuda=12.4` 行和 `nvidia` channel |
| **Linux** | 检查 `nvidia-smi` 确认 CUDA 版本，若 ≠ 12.4 则调整 `pytorch-cuda` 版本号 |

---

## 已知坑点（必须逐条遵守）

### 1. PyTorch 默认装成 CPU 版
**现象**：`torch.cuda.is_available()` 返回 `False`
**原因**：conda 解析 `pytorch>=2.0` 时优先选 CPU build
**解决**：`environment.yml` 中必须同时写：
```yaml
dependencies:
  - pytorch>=2.0
  - pytorch-cuda=12.4     # 强制选 CUDA 版
```
且 channels 要加 `nvidia`：
```yaml
channels:
  - pytorch
  - nvidia
  - conda-forge
  - defaults
```
**macOS 用户**：删掉 `pytorch-cuda=12.4` 和 `nvidia` channel

### 2. TensorBoard 启动报 `ModuleNotFoundError: No module named 'pkg_resources'`
**原因**：tensorboard 2.x 依赖已废弃的 `pkg_resources`，但 setuptools ≥ 80 移除了它
**解决**：锁定 `setuptools=75.6.0`
```yaml
dependencies:
  - setuptools=75.6.0
```

### 3. torchviz 需要系统级 graphviz
**现象**：`from torchviz import make_dot` 虽能 import，但调用 `make_dot()` 时报找不到 `dot`
**解决**：
```yaml
dependencies:
  - graphviz    # 不是 pip 包，是 conda 提供的系统级 graphviz
```
仅写 `pip install torchviz` 不够——那个只是 Python 绑定，`.exe` 需要系统装

### 4. `display()` 在纯 .py 脚本中报错
**现象**：`NameError: name 'display' is not defined`
**原因**：`display()` 是 IPython/Jupyter 专属函数，命令行 `python xx.py` 不认
**解决**：改 `display(df.head())` → `print(df.head())`

---

## 运行代码

每个子目录下：
```bash
cd code/work1          # 切到子目录
conda activate <name>  # 环境名见各 environment.yml 的 name 字段
python xxx.py          # 运行
```

---

## 排错流程（AI Agent 用）

当用户报告代码报错时，按顺序排查：

1. **环境是否激活** → 确认 `conda activate <name>`
2. **依赖是否装全** → 对照 `environment.yml` 逐项 `conda list`
3. **CUDA 是否可用** → `python -c "import torch; print(torch.cuda.is_available())"`
4. **graphviz 是否可用** → `where dot`（Windows）/ `which dot`（Unix）
5. **数据文件是否存在** → 检查代码中的 `.csv` 路径是否与实际文件名一致
6. **平台差异** → macOS 去 CUDA，Windows 注意路径反斜杠

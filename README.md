# AISec — 从机器学习到 AI 安全

使用 AI Agent 快速入门机器学习、深度学习。

本项目内置三个 Claude Code Skill 助教：

- **ml-tutor**：理论导师，讲解数学概念与模型原理，数学基础初中水平即可上手
- **mlcode-tutor**：代码导师，逐行讲解 PyTorch/TensorFlow 等 ML 代码实现
- **skill-auditor**：质量审计，7 维度结构化评估其他 Skill 的设计与实现质量

配套教材：[LeeDL Tutorial（李宏毅机器学习）](https://github.com/datawhalechina/leedl-tutorial/releases)，涵盖线性模型、深度学习基础到 RNN、CNN、GAN、BERT、Transformer、GPT 等一系列模型，非常适合深度学习入门。


## 使用`ml-tutor`入门理论知识

**前置要求**：安装 [Claude Code](https://docs.anthropic.com/claude-code)

```bash
git clone https://github.com/Erosion2020/AISec.git
cd AISec
```

下载配套教材 PDF 放置到 `AISec/LeeDL_Tutorial_v.1.2.4.pdf`，然后启动 Claude Code：

```bash
claude
```

进入 Claude Code 后，激活助教：

```
> /ml-tutor 初始化环境！
```

首次运行会引导完成初始化（学习进度记录、导师风格选择），之后直接接着上次进度继续。

直接告诉助教你想学什么：

```
> 梯度下降是什么意思，梯度下降和Loss函数有什么关系？
> 什么是反向传播，解释一下反向传播到底传递了哪些信息，反向传播在什么情况下可能导致信息传递丢失？
> 解释一下第60页中提到的softmax公式，这里用到的自然指数有何含义？
> 解释一下公式`L(θ) ≈ L(θ′) + (θ − θ′)ᵀg + 1/2 (θ − θ′)ᵀH(θ − θ′)`，该公式的三个项分别在计算什么？
```

## 使用`mlcode-tutor`

`code/work1/` 包含一个完整的 PyTorch 深度学习回归项目：

| 文件 | 说明 |
|---|---|
| `regression.py` | 完整训练流程：数据加载、模型定义、训练循环、TensorBoard 可视化 |
| `inference.py` | 独立推理脚本，加载已保存模型对新数据做预测 |
| `environment.yml` | Conda 环境配置，一键复现运行环境 |

```bash
# 创建环境并运行
conda env create -f code/work1/environment.yml
conda activate ml-env
python code/work1/regression.py
```

使用 mlcode-tutor 逐行讲解代码：

```
> /mlcode-tutor 帮我逐行分析 code/work1/regression.py
```

---

## 经典论文

### 基础必读（待补充）

- [Attention Is All You Need](paper/1706.03762v7.pdf) — Transformer 架构奠基之作
- [Sequence Level Training with Recurrent Neural Networks](https://arxiv.org/abs/1511.06732) — MIXER，序列级训练与 REINFORCE
- [The Curious Case of Neural Text Degeneration](https://arxiv.org/abs/1904.09751) — Nucleus Sampling (top-p)，解决文本生成退化
- [On Layer Normalization in the Transformer Architecture](https://arxiv.org/abs/2002.04745) — Pre-LN vs Post-LN 深度分析

### 进阶阅读（待补充）

- [Parallel Scheduled Sampling](https://arxiv.org/abs/1906.04331) — 并行化 Scheduled Sampling
- [Scheduled Sampling for Transformers](https://arxiv.org/abs/1906.07651) — 将 Scheduled Sampling 引入 Transformer
- [Rethinking and Improving NLG with Layer-Wise Multi-View Decoding](https://arxiv.org/abs/2005.08081) — 逐层多视图解码提升生成质量
- [DeepSeek V4 技术报告](paper/DeepSeek_V4.pdf) — 1.6T 参数 MoE，100 万上下文
- [Conditional Memory via Scalable Lookup](paper/2601.07372v1.pdf) — Engram，O(1) 查表的条件记忆模块

## 致谢

- **李宏毅老师** — 台湾大学机器学习方向教授，个人主页：[speech.ee.ntu.edu.tw/~tlkagk/](http://speech.ee.ntu.edu.tw/~tlkagk/)，YouTube：[@HungyiLeeNTU](https://www.youtube.com/@HungyiLeeNTU)
- **3Blue1Brown** — 数学家 Grant Sanderson 创立的数学科普频道，YouTube：[@3blue1brown](https://www.youtube.com/@3blue1brown)，Bilibili：[@3blue1brown](https://space.bilibili.com/88461692)
- **datawhalechina / leedl-tutorial** — 教材整理来源：[github.com/datawhalechina/leedl-tutorial](https://github.com/datawhalechina/leedl-tutorial)
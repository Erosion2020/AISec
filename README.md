# AISec — 从机器学习到 AI 安全

使用AI agent快速入门机器学习、深度学习。

本项目内置多个Claude Code Skill 助教 `ml-tutor`、`mlcode-tutor`，让它们来手把手带你你理解书中的理论、公式吧～


配套教材：[LeeDL Tutorial（李宏毅机器学习）](https://github.com/datawhalechina/leedl-tutorial/releases)，首先，把上述`Release`中的pdf放置到当前项目目录：`AISec/LeeDL_Tutorial_v.1.2.4.pdf`，然后在当前项目目录下启动`Claude Code`，就像这样：

该教材是李宏毅机器学习（深度学习）课程的提炼，包含从 从线性模型、深度学习基础 到 RNN、CNN、GAN、BERT、Transformer、GPT 等一系列深度学习模型。

--- 
**前置要求**：安装 [Claude Code](https://docs.anthropic.com/claude-code)


<details>
<summary><strong>QuickStart</strong></summary>

<br>


```bash
git clone https://github.com/Erosion2020/AISec.git
cd AISec
claude
```

进入 Claude Code 后，激活助教：

```
> /ml-tutor 初始化环境！
```

**首次运行**会经历三步初始化：

**① 询问是否记录学习进度**

```
顺便问一下——我可以在本地记录一点你的学习进度吗？这样下次继续学的时候，
我能知道你上次学到哪里、哪些概念已经熟了，不用从头开始。
文件只存在你自己的电脑上，你随时可以删。
```

输入 `可以` 或 `不用` 均可继续。

**② 选择导师性格**

```
我可以用不同的风格来陪你学，你喜欢哪种？

① 萌妹风格        — 软糯可爱，自称"人家"，全程充满元气和鼓励
② 李宏毅风格      — 台湾教授腔，口头禅是"神奇"和"大家"，爱用宝可梦/珍奶做类比
③ 东北妹子风格    — 豪爽直接，说话贼冲，但心眼儿贼好
④ 古板老教授风格  — 严肃正经，不废话，偶尔冷幽默
⑤ 嗲嗲台湾妹风格  — 台湾腔，尾音上扬，"欸你知道吗"，让人觉得很放松
```

输入序号即可，例如 `3`。

**③ 初始化完成，开始提问**

以东北妹子为例：

```
哎，嘎哈呢老铁？现在在整哪块儿？还是有啥整不明白的地方？说来听听呗！
```

直接告诉助教你在学什么，或者给出 PDF 页码：

```
> 帮我看第 30 页
> 梯度下降是什么意思
> 我不懂反向传播
```

**第二次及以后启动**，profile 已缓存，直接跳过初始化，上来就能接着上次的进度继续。

</details>

---

## 经典论文

<details>
<summary><strong>必读论文</strong></summary>

<br>

- [Attention Is All You Need](paper/1706.03762v7.pdf) — Transformer 架构奠基之作
- [DeepSeek V4 技术报告](paper/DeepSeek_V4.pdf) — 1.6T 参数 MoE，100 万上下文
- [Conditional Memory via Scalable Lookup](paper/2601.07372v1.pdf) — Engram，O(1) 查表的条件记忆模块

</details>

<details>
<summary><strong>经典论文</strong></summary>

<br>

- [Sequence Level Training with Recurrent Neural Networks](https://arxiv.org/abs/1511.06732) — MIXER，序列级训练与 REINFORCE
- [The Curious Case of Neural Text Degeneration](https://arxiv.org/abs/1904.09751) — Nucleus Sampling (top-p)，解决文本生成退化
- [Parallel Scheduled Sampling](https://arxiv.org/abs/1906.04331) — 并行化 Scheduled Sampling
- [Scheduled Sampling for Transformers](https://arxiv.org/abs/1906.07651) — 将 Scheduled Sampling 引入 Transformer
- [On Layer Normalization in the Transformer Architecture](https://arxiv.org/abs/2002.04745) — Pre-LN vs Post-LN 深度分析
- [Rethinking and Improving NLG with Layer-Wise Multi-View Decoding](https://arxiv.org/abs/2005.08081) — 逐层多视图解码提升生成质量

</details>

---

## 数学内容专栏（待完善）

### 线性代数（3Blue1Brown）
 - 序言
 - 向量究竟是什么？
 - 线性组合、张成的空间与基
 - 矩阵与线性变换
 - 矩阵乘法与线性变换复合
    - 三维空间中的线性变换
 - 行列式
 - 逆矩阵、列空间与零空间
    - 非方阵
 - 点积与对偶性
 - 叉积的标准介绍
 - 以线性变换的眼光看叉积
 - 基变换
 - 特征向量与特征值
 - 抽象向量空间
 - 克莱姆法则，几何解释

### 微积分
### 概率论与数理统计

### 书中的数学公式解读

 - 微分

## 致谢

- **李宏毅老师** — 台湾大学机器学习方向教授，个人主页：[speech.ee.ntu.edu.tw/~tlkagk/](http://speech.ee.ntu.edu.tw/~tlkagk/)，YouTube：[@HungyiLeeNTU](https://www.youtube.com/@HungyiLeeNTU)
- **3Blue1Brown** - 数学家Grant Sanderson创立的数学科普频道，youtube主页：[youtube@3blue1brown](https://www.youtube.com/@3blue1brown)、[bilibili@3blue1brown](https://space.bilibili.com/88461692?spm_id_from=333.337.0.0)
- **datawhalechina / leedl-tutorial** — 教材整理来源：[github.com/datawhalechina/leedl-tutorial](https://github.com/datawhalechina/leedl-tutorial)

# AISec — 从机器学习到 AI 安全

建立本仓库的目的是在AI时代通过使用`AI Agent`的方式来帮助你掌握更深层次的AI技能（深度学习方向），那么首先需要声明的一点是 我会假设你的数学水平只有初高中水平，你从未接触过`高等数学`、`线性代数`、`概率与数理统计`、`微积分`等这些看起来学习深度学习所必要掌握的内容。

我需要提前声明一点的 是你不会这些基础学科完全没有关系，但是你也要做好十足的准备来迎接一些挑战～

<details>
<summary><strong>关于AI时代的学习建议</strong></summary>

<br>


先来谈谈深度学习本身吧，如果你真的想要掌握深度学习的内容，千万不要直接搜索一些国内的关于这些基础学科的知识，国内的很多教程大多是基于让你考试拿高分的目标进行教学，比如你可能会学到关于微积分和线性代数的一些计算技巧，但是学习这些计算技巧并不会让你在深度学习中有更好的理解。

我想～更重要的一点是，如果只是单纯学习这些关于定义和计算的内容 过程一定是困难和枯燥的，真的很难坚持学习下去～

你需要建立的应该是对于这些学科"本质"的理解，比如 在线性代数中 你应该理解`向量`、`矩阵`其实就是用来描述多维度空间中一系列数据的一种表示方法，我假设你已经理解了`空间`的概念，那么我想你再去看一下关于向量或者矩阵的 `加法`、`点积`、`行列式`、`秩`，你应该就可以体会到很大的兴趣，你会发现原来`空间世界`如此美妙～

本仓库同时会涵盖这部分的数学内容，关于`微积分`、`线性代数`的大多数内容都来自于`3Blue1Brown`，我真的非常推荐你学习这个博主的数学知识，如果你的英文不太好 那么你可以找到`B站大学`中`婆婆町`这位UP提供的汉化版本～

现在这个时代学习的方法已经和以前不太一样，你完全不需要补充所有的基础知识才能开始学习一门看起来比较高深的学习，我们通过借助于 `AI Agent`的能力，完全可以在没有任何基础的情况下进行学习，如果你发现你有一块知识缺失了，只需要借助它的能力 让自己快速补充这部分知识点就行了～

另外我还想特别补充一点的是，千万不要在学习过程中 尝试独自陷入一个问题的研究而浪费太多时间，也不要过于深入研究某一个数学或者其他领域。我为什么这么说呢？其实这来自于我觉得的一个比较震撼的消息，`2026-05-21`这个时间节点上OpenAI使用内部特供的GPT模型解决了`埃尔德什平面单位距离问题`，我查了一下相关资料 发现该问题居然是一个准菲尔兹奖级别的研究成果，这个消息对我的冲击力有点过于大了。

我一直觉得AI能够取代工程级工作 比如我之前写后端代码的工作，甚至也能够取代一些比较`水`的科研工作，但是谁能想到AI竟然也能做如此前沿高端的科研工作，真的有点`AlphoGO`突破到`AlphaGO Zero`的感觉了。

说实话，AI每次突破我的认知边界，都会带来这种冲击感——回头看，这种"被颠覆"的瞬间已经不是第一次了。

遥想最开始我还无法接受自己刷了几百道的算法题，写了一堆自认为质量很高的代码，直到后来才发现 自己所谓比较难解决的问题或者算法，AI仅仅几十秒钟就能解决。

hh～ 现在已经释然了，AI时代个人感觉如果你想学习，建议可以有两个方向（个人主观）：

 - （偏工作）学一些自己从前根本学不会的内容，借助AI可以快速掌握多个领域的知识，复合型
 - （偏个人）爱好什么就学什么吧，释然一点，喜欢学音乐就学音乐，喜欢学围棋就学围棋，别人的评论对于AI时代已没有什么必要性。


</details>

--- 

<details>
<summary><strong>QuickStart</strong></summary>

<br>

**前置要求**：已安装 [Claude Code](https://docs.anthropic.com/claude-code)

本仓库依赖于李宏毅教授的机器学习课程，从线性模型一路到 Transformer、生成模型，最终落到 AI 安全的应用场景。内置了一个 Claude Code Skill 助教 `ml-tutor`，数学基础初中水平即可上手——把不懂的概念或 PDF 页码直接丢给它就行。但首先你需要下载一下对应的教学书籍（我为了让当前项目看起来没有那么大，并没有在项目内内置对应的教材）

配套教材：[LeeDL Tutorial（李宏毅机器学习）](https://github.com/datawhalechina/leedl-tutorial/releases)，首先，把上述`Release`中的pdf放置到当前项目目录：`AISec/LeeDL_Tutorial_v.1.2.4.pdf`，然后在当前项目目录下启动`Claude Code`，就像这样：


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

## 数学内容专栏

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

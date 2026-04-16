# AISec — 从机器学习到 AI 安全

配套教材：[LeeDL Tutorial（李宏毅深度学习）](https://github.com/datawhalechina/leedl-tutorial/releases)

本仓库跟着李宏毅深度学习课程走，从线性模型一路到 Transformer、生成模型，最终落到 AI 安全的应用场景。内置了一个 Claude Code Skill 助教 `ml-tutor`，数学基础初中水平即可上手——把不懂的概念或 PDF 页码直接丢给它就行。

---

<details>
<summary><strong>QuickStart — 启动 ml-tutor 助教</strong></summary>

<br>

**前置要求**：已安装 [Claude Code](https://docs.anthropic.com/claude-code)

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

## 致谢

- **李宏毅老师** — 台湾大学教授，课程主页：[speech.ee.ntu.edu.tw/~hylee/ml](https://speech.ee.ntu.edu.tw/~hylee/ml/)，YouTube：[@HungyiLeeNTU](https://www.youtube.com/@HungyiLeeNTU)
- **datawhalechina / leedl-tutorial** — 教材整理来源：[github.com/datawhalechina/leedl-tutorial](https://github.com/datawhalechina/leedl-tutorial)

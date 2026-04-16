# 课程地图：李宏毅深度学习（LeeDL Tutorial）

本文件用于：规划学习路径、了解前置依赖、定位用户问题所在章节。

---

## 课程模块与章节

### 第一部分：机器学习基础
- 什么是机器学习（监督 / 无监督 / 强化学习）
- 回归（Regression）
- 分类（Classification）
- 损失函数（Loss Function）
- 梯度下降（Gradient Descent）

### 第二部分：深度学习基础
- 神经网络结构与前向传播
- 激活函数（Sigmoid、ReLU、Tanh）
- 反向传播（Backpropagation）
- 批归一化（Batch Normalization）

### 第三部分：模型优化
- 学习率调整（Learning Rate Scheduling）
- 优化器（SGD、Adam、RMSprop）
- 正则化（Regularization）与 Dropout

### 第四部分：卷积神经网络（CNN）
- 卷积层原理与池化层
- 经典架构（LeNet、ResNet 等）

### 第五部分：循环神经网络（RNN）
- RNN 基础
- LSTM / GRU
- 序列到序列模型

### 第六部分：自注意力与 Transformer
- Self-Attention 原理
- Transformer 架构
- BERT 预训练

### 第七部分：生成模型
- GAN（生成对抗网络）
- VAE（变分自编码器）
- Diffusion Model

---

## 概念前置依赖

学某个概念之前，需要先理解哪些基础。
若学生跳过前置直接问高级概念，建议先补足前置再继续。

```
梯度下降
  └─ 前置：导数的直觉（变化率）→ 读 references/math/calculus.md

反向传播
  └─ 前置：梯度下降、链式法则 → 读 references/math/calculus.md

激活函数（Sigmoid / ReLU）
  └─ 前置：神经网络前向传播的基本结构

损失函数（交叉熵）
  └─ 前置：概率分布的直觉 → 读 references/math/probability.md

Self-Attention
  └─ 前置：矩阵乘法的含义（变换叠加）→ 读 references/math/linear-algebra.md

Transformer
  └─ 前置：Self-Attention

BERT / 大模型预训练
  └─ 前置：Transformer 架构

GAN
  └─ 前置：损失函数、梯度下降

Diffusion Model
  └─ 前置：概率分布、期望 → 读 references/math/probability.md

批归一化（Batch Norm）
  └─ 前置：均值与方差的含义（初中统计）

Adam 优化器
  └─ 前置：梯度下降、动量的直觉
```

---

## 推荐学习路径（数学薄弱起点）

```
① 梯度下降（直觉） → ② 损失函数 → ③ 神经网络前向传播
→ ④ 激活函数 → ⑤ 反向传播 → ⑥ 优化器
→ ⑦ CNN → ⑧ Self-Attention → ⑨ Transformer
```

遇到数学卡壳时，根据关键词路由到对应的 math/ 文件补课，补完后回到主线。

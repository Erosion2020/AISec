# PyTorch 常用模式

---

## 模型定义

### `nn.Module` 继承模板
```python
class MyModel(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(input_dim, 16),
            nn.ReLU(),
            nn.Linear(16, 8),
            nn.ReLU(),
            nn.Linear(8, 1)
        )

    def forward(self, x):
        x = self.layers(x)
        x = x.squeeze(1)
        return x
```
- `__init__`：定义层结构
- `forward`：定义前向传播的计算顺序
- **不要直接在 `forward` 里创建新的 layer**（会被重复创建）

### `nn.Sequential` vs 手动 forward
- `nn.Sequential`：顺序执行各层，适合简单的前馈网络
- 手动 `forward`：可以写分支、跳连、自定义计算，适合复杂结构

### `nn.Linear(in_features, out_features)`
- 全连接层（线性层），参数 `in` → `out`
- `nn.Linear(118, 16)`：118 个输入特征 → 16 个输出神经元
- 注意**维度匹配**：上一层的 out 必须等于下一层的 in

### `.squeeze(dim)`
- 移除指定维度上大小为 1 的维度
- `(B, 1)` → `.squeeze(1)` → `(B,)`
- 回归输出通常需要 squeeze，因为 `nn.Linear(N, 1)` 输出的是 `(batch, 1)` 而标签是 `(batch,)`

---

## Dataset & DataLoader

### Dataset 模板
```python
class MyDataset(Dataset):
    def __init__(self, x, y=None):
        self.y = None if y is None else torch.FloatTensor(y)
        self.x = torch.FloatTensor(x)

    def __getitem__(self, idx):
        if self.y is None:
            return self.x[idx]
        return self.x[idx], self.y[idx]

    def __len__(self):
        return len(self.x)
```
- 必须实现 `__len__` 和 `__getitem__`
- `y=None` 的情况用于**测试集**（没有标签），只返回 x
- `torch.FloatTensor()` 将 NumPy 转为 float32 张量

### DataLoader 参数
```python
DataLoader(dataset, batch_size=256, shuffle=True, pin_memory=True)
```
- `batch_size`：每次取多少条数据
- `shuffle`：训练时 True（打乱顺序），验证/测试时 False
- `pin_memory=True`：加速 CPU→GPU 传输（锁页内存）

---

## 训练流程

### 标准训练循环
```python
for x, y in train_loader:           # 取一个 batch
    optimizer.zero_grad()            # ① 清空梯度（Pytorch默认累积梯度）
    x, y = x.to(device), y.to(device)  # ② 移到 GPU
    pred = model(x)                  # ③ 前向传播
    loss = criterion(pred, y)        # ④ 计算损失
    loss.backward()                  # ⑤ 反向传播（计算梯度）
    optimizer.step()                 # ⑥ 更新参数
```
这个顺序是固定的，缺一步都会出问题。最常见的错误是**忘记 `optimizer.zero_grad()`**——PyTorch 默认会累积梯度而不是清零。

### 验证时不需要梯度
```python
model.eval()
with torch.no_grad():
    pred = model(x)
    loss = criterion(pred, y)
```
- `model.eval()` 关闭 BN/Dropout 的训练行为
- `torch.no_grad()` 不构建计算图，节省显存

### 早停 (Early Stopping)
```python
if mean_valid_loss < best_loss:
    best_loss = mean_valid_loss
    torch.save(model.state_dict(), 'model.ckpt')
    early_stop_count = 0
else:
    early_stop_count += 1

if early_stop_count >= config['early_stop']:
    return  # 停止训练
```
- 验证损失不下降就计数，连续 N 轮不降就停
- `model.state_dict()` 只保存参数（不含结构），比保存整个模型更小更灵活

---

## 常用工具

### 固定随机种子
```python
torch.backends.cudnn.deterministic = True    # cuDNN 使用确定性算法
torch.backends.cudnn.benchmark = False       # 关闭自动算法搜索
np.random.seed(seed)
torch.manual_seed(seed)
torch.cuda.manual_seed_all(seed)             # 多 GPU 时全部设置
```

### TensorBoard 记录
```python
writer = SummaryWriter()
writer.add_scalar('Loss/train', loss_value, step)
```
- `add_scalar` 记录标量（损失、准确率等），在 TensorBoard 中画曲线
- `step` 是 x 轴的值（通常是 epoch 或 global step）

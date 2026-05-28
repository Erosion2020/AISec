# Python 语法基础

ML 代码中常见但新手可能不熟悉的 Python 语法，按出现频率排列。

---

## 类与继承

### `class MyModel(nn.Module):`
- `class` 定义一个类（蓝图），`MyModel` 是类名
- 括号里的 `nn.Module` 是**父类**，意味着 `MyModel` 继承了 `nn.Module` 的所有功能
- 对 ML 代码：大部分模型都继承 `nn.Module`(PyTorch) 或 `tf.keras.Model`(TensorFlow)

### `super().__init__()`
- 调用父类的 `__init__` 方法，完成父类的初始化
- ML 代码中几乎每个模型的 `__init__` 开头都有这行——它注册模型参数，让框架知道要追踪哪些层
- **忘写这行会导致模型参数无法被 optimizer 找到**

### `__init__`, `__getitem__`, `__len__`
- 双下划线开头结尾的方法是 Python 的**特殊方法**（dunder methods）
- `__init__`：创建实例时自动调用（构造函数）
- `__getitem__(self, idx)`：让对象支持 `obj[0]` 这种索引写法，PyTorch Dataset 必须实现
- `__len__(self)`：让对象支持 `len(obj)`，PyTorch Dataset 必须实现

---

## 装饰器

### `@torch.no_grad()`
- `@` 是装饰器语法，等价于把下面的函数包了一层
- `torch.no_grad()` 在推理/验证时**关闭梯度计算**，节省显存和计算
- 训练时不加这个，验证时一定要加

---

## 常见模式

### `if __name__ == '__main__':`
- 判断这个文件是被直接运行（`python xxx.py`）还是被 import 导入
- 当直接运行时条件为 True，当被其他文件 import 时条件为 False
- 通常把测试代码或主入口放在这个 if 块里

### `model.train()` vs `model.eval()`
- `model.train()`：开启训练模式（BN 层和 Dropout 正常工作）
- `model.eval()`：开启评估模式（BN 用统计值，Dropout 关闭）
- **训练前调 `.train()`，验证/推理前调 `.eval()`**，不然结果会不对

### `.to(device)`
- 把张量或模型移到指定设备（CPU 或 GPU）
- `device = 'cuda' if torch.cuda.is_available() else 'cpu'`
- 模型和数据必须在**同一个设备**上才能计算

### `.detach().cpu().numpy()`
- `.detach()`：从计算图中分离（不再追踪梯度）
- `.cpu()`：从 GPU 移到 CPU
- `.numpy()`：转成 NumPy 数组
- 三步连写是把 GPU 上的 PyTorch 张量转成 CPU 上的 NumPy 数组的标准写法

---

## 生成器与迭代

### `random_split(dataset, [a, b])`
- PyTorch 的 `random_split` 返回的是 `Subset` 对象，不是数组
- 后续使用需要转成你需要的格式（常见的是 `np.array()`）

### `tqdm(iterable)`
- 包装任何可迭代对象，显示进度条
- `position=0` 控制进度条位置，`leave=True` 完成后保留进度条
- `set_description()` 设置左边文字，`set_postfix()` 设置右边文字

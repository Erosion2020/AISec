# NumPy & Pandas 常用模式

---

## NumPy

### `np.array(data)`
- 将数据转为 NumPy 多维数组（ndarray）
- `.shape` → 查看维度，如 `(2699, 118)` 表示 2699 行 118 列
- 切片：`data[:, :-1]` → 所有行，去掉最后一列；`data[:, -1]` → 所有行，只取最后一列

### `np.random.seed(seed)`
- 固定 NumPy 的随机数生成器的种子值
- 确保每次运行产生的随机结果一致（可复现）

### `list(range(n))`
- `range(n)` 生成 0 到 n-1 的整数序列
- `list()` 把它转成列表

---

## Pandas

### `pd.read_csv('file.csv')`
- 读取 CSV 文件，返回 DataFrame（表格结构，有行有列）
- `pd.read_csv('./covid.train.csv')` 读训练集，`pd.read_csv('./covid.test.csv')` 读测试集

### `df.head(n)`
- 显示 DataFrame 的前 n 行，默认 5 行
- 用于快速预览数据长什么样

### `df.values`
- 把 DataFrame 转成 NumPy ndarray，**丢失列名信息**
- 后续用 NumPy 运算时需要这一步

### `pd.set_option('display.max_column', N)`
- 设置 Pandas 显示的最大列数
- 默认只显示 20 列，ML 数据通常有几十甚至上百列特征，所以需要调大
- 其他常用 option：`'display.max_rows'`（最大行数）、`'display.width'`（总宽度）

### `display()`
- 在 Jupyter/IPython 环境中格式化显示对象（比 `print` 更好看的表格）
- 普通 Python 脚本中 `display()` 也能工作（IPython 环境），但在纯命令行脚本里可能不生效

---

## 常见组合操作

### 读取 → 预览 → 转 NumPy → 释放内存
```python
train_df = pd.read_csv('./covid.train.csv')  # 读成 DataFrame
display(train_df.head(3))                     # 看前 3 行
train_data = train_df.values                  # 转成 NumPy
del train_df                                  # 释放 DataFrame 内存
```
- `del` 手动释放变量占用的内存，对大文件有用
- 注意：转 `.values` 之后就不再需要 Pandas 的列名等功能了

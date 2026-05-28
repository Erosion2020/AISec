# Scikit-learn 常用模式

---

## 数据预处理

### `train_test_split`
```python
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```
- `test_size`：测试集比例
- `random_state`：随机种子，保证每次拆分一致

### 标准化/归一化
```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)  # 在训练集上 fit + transform
X_test = scaler.transform(X_test)        # 测试集只用 transform（不要fit）
```
- `StandardScaler`：减均值除以标准差 → 均值 0 方差 1
- `MinMaxScaler`：缩放到 [0, 1] 区间
- **关键**：测试集用训练集的统计量，不要对测试集单独 fit

---

## 模型

### 线性模型
```python
from sklearn.linear_model import LinearRegression, Ridge, Lasso
model = LinearRegression()
model.fit(X_train, y_train)
preds = model.predict(X_test)
```
- `Ridge`：带 L2 正则的线性回归
- `Lasso`：带 L1 正则的线性回归（能做特征选择）

### 树模型
```python
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
```
- `n_estimators`：树的数量，越多越稳定但越慢

---

## 评估指标

```python
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
mse = mean_squared_error(y_true, y_pred)
mae = mean_absolute_error(y_true, y_pred)
r2 = r2_score(y_true, y_pred)
```
- MSE：均方误差（对异常值敏感）
- MAE：平均绝对误差（更鲁棒）
- R²：越接近 1 越好，负值表示模型比直接用均值还差

---

## Pipeline

```python
from sklearn.pipeline import Pipeline
pipe = Pipeline([
    ('scaler', StandardScaler()),
    ('model', LinearRegression())
])
pipe.fit(X_train, y_train)
preds = pipe.predict(X_test)
```
- 把预处理和模型打包，避免测试集上忘记 transform

---

## 特征选择

### `SelectKBest`
```python
from sklearn.feature_selection import SelectKBest, f_regression
selector = SelectKBest(f_regression, k=10)
X_new = selector.fit_transform(X, y)
```
- 选出与目标相关性最高的 k 个特征

### 互信息
```python
from sklearn.feature_selection import mutual_info_regression
mi = mutual_info_regression(X, y)  # 返回每个特征与目标的互信息值
```
- 比相关系数更能捕获非线性关系

"""
regression.py 的独立推理脚本。
不需要重新训练，只加载已保存的模型对新数据做预测。

用法：
    python inference.py                          # 使用默认路径
    python inference.py --input new_data.csv     # 指定输入文件
    python inference.py --input test.csv --output result.csv --device cuda
"""
import argparse
import csv
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from tqdm import tqdm


# ============================================================
# 模型定义（与 regression.py 中 My_Model 完全一致）
# ============================================================
class My_Model(nn.Module):
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
        x = x.squeeze(1)  # (B, 1) -> (B,)
        return x


# ============================================================
# 数据集（与 regression.py 中 COVID19Dataset 一致，仅预测模式）
# ============================================================
class PredictDataset(Dataset):
    """仅特征、无标签的预测数据集"""
    def __init__(self, x):
        self.x = torch.FloatTensor(x)

    def __getitem__(self, idx):
        return self.x[idx]

    def __len__(self):
        return len(self.x)


# ============================================================
# 预测函数（与 regression.py 中 predict 一致）
# ============================================================
def predict(loader, model, device):
    model.eval()
    preds = []
    for x in tqdm(loader, desc='Predicting'):
        x = x.to(device)
        with torch.no_grad():
            pred = model(x)
            preds.append(pred.detach().cpu())
    return torch.cat(preds, dim=0).numpy()


# ============================================================
# 保存结果
# ============================================================
def save_pred(preds, file):
    with open(file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'tested_positive'])
        for i, p in enumerate(preds):
            writer.writerow([i, p])
    print(f'Results saved to: {file}')


# ============================================================
# 主流程
# ============================================================
def main():
    parser = argparse.ArgumentParser(description='COVID-19 阳性率预测推理')
    parser.add_argument('--input',  default='./covid.test.csv', help='输入 CSV 路径（117 列特征）')
    parser.add_argument('--model',  default='./models/model.ckpt', help='模型权重路径')
    parser.add_argument('--output', default='./pred.csv', help='预测结果输出路径')
    parser.add_argument('--device', default='cuda', choices=['cuda', 'cpu'], help='推理设备')
    parser.add_argument('--batch-size', type=int, default=256, help='批量大小')
    args = parser.parse_args()

    # 设备选择
    device = args.device if args.device == 'cpu' or torch.cuda.is_available() else 'cpu'
    print(f'Device: {device}')

    # 加载数据
    print(f'Loading: {args.input}')
    data = np.genfromtxt(args.input, delimiter=',', skip_header=1)  # 跳过表头
    if data.ndim == 1:
        data = data.reshape(1, -1)
    n_samples, n_features = data.shape
    print(f'Samples: {n_samples}, Features: {n_features}')

    # 加载模型
    print(f'Loading model: {args.model}')
    model = My_Model(input_dim=n_features).to(device)
    model.load_state_dict(torch.load(args.model, map_location=device, weights_only=True))
    model.eval()

    # 构造 DataLoader
    dataset = PredictDataset(data)
    loader = DataLoader(dataset, batch_size=args.batch_size, shuffle=False)

    # 推理
    preds = predict(loader, model, device)
    print(f'Predictions: min={preds.min():.4f}, max={preds.max():.4f}, mean={preds.mean():.4f}')

    # 保存
    save_pred(preds, args.output)


if __name__ == '__main__':
    main()

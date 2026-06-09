import os
import random
#导入pytorch
import torch
#导入进度条
from tqdm import tqdm

# 脚本所在目录，用于构造数据路径（兼容从任意CWD运行）
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# 定义导入feature函数
def load_feat(path):
    feat = torch.load(path)
    return feat

def shift(x, n):
    if n < 0:
        left = x[0].repeat(-n, 1)
        right = x[:n]

    elif n > 0:
        right = x[-1].repeat(n, 1)
        left = x[n:]
    else:
        return x

    return torch.cat((left, right), dim=0)
# 将前后的特征联系在一起，如concat_n = 11 则前后都接5
def concat_feat(x, concat_n):
    assert concat_n % 2 == 1 # n 必须是奇数
    if concat_n < 2:
        return x
    seq_len, feature_dim = x.size(0), x.size(1)
    x = x.repeat(1, concat_n) 
    x = x.view(seq_len, concat_n, feature_dim).permute(1, 0, 2) # concat_n, seq_len, feature_dim
    mid = (concat_n // 2)
    for r_idx in range(1, mid+1):
        x[mid + r_idx, :] = shift(x[mid + r_idx], r_idx)
        x[mid - r_idx, :] = shift(x[mid - r_idx], -r_idx)

    return x.permute(1, 0, 2).view(seq_len, concat_n * feature_dim)

# 数据预处理函数
def preprocess_data(split, feat_dir, phone_path, concat_nframes, train_ratio=0.8, train_val_seed=1337):
    class_num = 41 # NOTE: 预先计算，不需要更改
    mode = 'train' if (split == 'train' or split == 'val') else 'test'

    label_dict = {}
    if mode != 'test':
      phone_file = open(os.path.join(phone_path, f'{mode}_labels.txt')).readlines()

      for line in phone_file:
          line = line.strip('\n').split(' ')
          label_dict[line[0]] = [int(p) for p in line[1:]]

    if split == 'train' or split == 'val':
        # 分割训练和验证数据
        usage_list = open(os.path.join(phone_path, 'train_split.txt')).readlines()
        random.seed(train_val_seed)
        random.shuffle(usage_list)
        percent = int(len(usage_list) * train_ratio)
        usage_list = usage_list[:percent] if split == 'train' else usage_list[percent:]
    elif split == 'test':
        usage_list = open(os.path.join(phone_path, 'test_split.txt')).readlines()
    else:
        raise ValueError('Invalid \'split\' argument for dataset: PhoneDataset!')

    usage_list = [line.strip('\n') for line in usage_list]
    print('[Dataset] - # phone classes: ' + str(class_num) + ', number of utterances for ' + split + ': ' + str(len(usage_list)))

    max_len = 3000000
    X = torch.empty(max_len, 39 * concat_nframes)
    if mode != 'test':
      y = torch.empty(max_len, dtype=torch.long)

    idx = 0
    for i, fname in tqdm(enumerate(usage_list)):
        feat = load_feat(os.path.join(feat_dir, mode, f'{fname}.pt'))
        cur_len = len(feat)
        feat = concat_feat(feat, concat_nframes)
        if mode != 'test':
          label = torch.LongTensor(label_dict[fname])

        X[idx: idx + cur_len, :] = feat
        if mode != 'test':
          y[idx: idx + cur_len] = label

        idx += cur_len

    X = X[:idx, :]
    if mode != 'test':
      y = y[:idx]

    print(f'[INFO] {split} set')
    print(X.shape)
    if mode != 'test':
      print(y.shape)
      return X, y
    else:
      return X
# 返回的X代表数据的维度，如果不链接则为39 如果链接即为n*39 n为连接的特征总数,y为标签

import torch
#导入数据集
from torch.utils.data import Dataset
#导入数据加载工具Dataloader
from torch.utils.data import DataLoader
#定义数据集，一个数据集类应该包含初始化，_getitem__（获取一个元素）以及__len__（获取数据长度）方法
class LibriDataset(Dataset):
    def __init__(self, X, y=None):
        self.data = X
        if y is not None:
            self.label = torch.LongTensor(y)
        else:
            self.label = None

    def __getitem__(self, idx):
        if self.label is not None:
            return self.data[idx], self.label[idx]
        else:
            return self.data[idx]

    def __len__(self):
        return len(self.data)
import torch
import torch.nn as nn
# 建立神经网络
class BasicBlock(nn.Module):# 继承 torch 的 Module
    def __init__(self, input_dim, output_dim):
        super(BasicBlock, self).__init__()

        self.block = nn.Sequential(
            nn.Linear(input_dim, output_dim),
            nn.ReLU(),
        )

    def forward(self, x):
        x = self.block(x)
        return x


class Classifier(nn.Module):
    def __init__(self, input_dim, output_dim=41, hidden_layers=1, hidden_dim=256):
        super(Classifier, self).__init__()

        self.fc = nn.Sequential(
            BasicBlock(input_dim, hidden_dim),
            *[BasicBlock(hidden_dim, hidden_dim) for _ in range(hidden_layers)], # *[]将循环得到的解压
            nn.Linear(hidden_dim, output_dim)
        )

    def forward(self, x):
        x = self.fc(x)
        return x
    
# data prarameters
# 用于数据处理时的参数
concat_nframes = 1              # 要连接的帧数,n必须为奇数（总共2k+1=n帧）
train_ratio = 0.8               # 用于训练的数据比率，其余数据将用于验证
# training parameters
# 训练过程中的参数
seed = 0                        # 随机种子
batch_size = 512                # 批次数目
num_epoch = 5                   # 训练epoch数
learning_rate = 0.0001          # 学习率
models_dir = os.path.join(SCRIPT_DIR, 'models')
if not os.path.isdir(models_dir):
        # 创建文件夹-用于存储模型
    os.mkdir(models_dir)
model_path = os.path.join(models_dir, 'model.ckpt')  # 保存在脚本所在目录
# model parameters
# 模型参数
input_dim = 39 * concat_nframes # 模型的输入维度，不应更改该值，这个值由上面的拼接函数决定
hidden_layers = 1               # hidden_layer层的数量
hidden_dim = 256                # 隐藏维度

# 引入gc模块进行垃圾回收
import gc

# 预处理数据
train_X, train_y = preprocess_data(split='train', feat_dir=os.path.join(SCRIPT_DIR, 'data/libriphone/feat'), phone_path=os.path.join(SCRIPT_DIR, 'data/libriphone'), concat_nframes=concat_nframes, train_ratio=train_ratio)
val_X, val_y = preprocess_data(split='val', feat_dir=os.path.join(SCRIPT_DIR, 'data/libriphone/feat'), phone_path=os.path.join(SCRIPT_DIR, 'data/libriphone'), concat_nframes=concat_nframes, train_ratio=train_ratio)

# 将数据导入
train_set = LibriDataset(train_X, train_y)
val_set = LibriDataset(val_X, val_y)

# 删除原始数据以节省内存
del train_X, train_y, val_X, val_y
gc.collect()

# 利用dataloader加载数据
train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True)
val_loader = DataLoader(val_set, batch_size=batch_size, shuffle=False)

# 检查当前是否有可用的GPU 否则使用CPU
device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
print(f'DEVICE: {device}')

import numpy as np

# 固定随机种子
def same_seeds(seed): # 固定随机种子（CPU）
    torch.manual_seed(seed) # 固定随机种子（GPU)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed) # 为当前GPU设置
        torch.cuda.manual_seed_all(seed)  # 为所有GPU设置
    np.random.seed(seed)  # 保证后续使用random函数时，产生固定的随机数
    torch.backends.cudnn.benchmark = False # GPU、网络结构固定，可设置为True
    torch.backends.cudnn.deterministic = True # 固定网络结构

# 固定随机种子
same_seeds(seed)

# 创建模型、定义损失函数和优化器
model = Classifier(input_dim=input_dim, hidden_layers=hidden_layers, hidden_dim=hidden_dim).to(device)
criterion = nn.CrossEntropyLoss() 
optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)

best_acc = 0.0
for epoch in range(num_epoch):
    train_acc = 0.0
    train_loss = 0.0
    val_acc = 0.0
    val_loss = 0.0
    
    # 训练部分
    model.train() # 设定模型到训练模式
    for i, batch in enumerate(tqdm(train_loader)):
        features, labels = batch
        features = features.to(device)
        labels = labels.to(device)
        
        optimizer.zero_grad() 
        outputs = model(features) 
        
        loss = criterion(outputs, labels)
        loss.backward() 
        optimizer.step() 
        
        _, train_pred = torch.max(outputs, 1) # 获得概率最高的类的索引
        train_acc += (train_pred.detach() == labels.detach()).sum().item()
        train_loss += loss.item()
    
    # 验证部分
    if len(val_set) > 0:
        model.eval() # 设定模型到评估模式
        with torch.no_grad():
            for i, batch in enumerate(tqdm(val_loader)):
                features, labels = batch
                features = features.to(device)
                labels = labels.to(device)
                outputs = model(features)
                
                loss = criterion(outputs, labels) 
                
                _, val_pred = torch.max(outputs, 1) 
                val_acc += (val_pred.cpu() == labels.cpu()).sum().item() # 获得概率最高的类的索引
                val_loss += loss.item()

            print('[{:03d}/{:03d}] Train Acc: {:3.6f} Loss: {:3.6f} | Val Acc: {:3.6f} loss: {:3.6f}'.format(
                epoch + 1, num_epoch, train_acc/len(train_set), train_loss/len(train_loader), val_acc/len(val_set), val_loss/len(val_loader)
            ))

            # 如果模型获得提升，在此阶段保存模型
            if val_acc > best_acc:
                best_acc = val_acc
                torch.save(model.state_dict(), model_path)
                print('saving model with acc {:.3f}'.format(best_acc/len(val_set)))
    else:
        print('[{:03d}/{:03d}] Train Acc: {:3.6f} Loss: {:3.6f}'.format(
            epoch + 1, num_epoch, train_acc/len(train_set), train_loss/len(train_loader)
        ))

# 如果结束验证，则保存最后一个epoch得到的模型
if len(val_set) == 0:
    torch.save(model.state_dict(), model_path)
    print('saving model at last epoch')
del train_loader, val_loader
gc.collect()

# 载入数据
test_X = preprocess_data(split='test', feat_dir=os.path.join(SCRIPT_DIR, 'data/libriphone/feat'), phone_path=os.path.join(SCRIPT_DIR, 'data/libriphone'), concat_nframes=concat_nframes)
test_set = LibriDataset(test_X, None)
test_loader = DataLoader(test_set, batch_size=batch_size, shuffle=False)

# 加载已经训练好的模型
model = Classifier(input_dim=input_dim, hidden_layers=hidden_layers, hidden_dim=hidden_dim).to(device)
model.load_state_dict(torch.load(model_path))

test_acc = 0.0
test_lengths = 0
pred = np.array([], dtype=np.int32)

model.eval()
with torch.no_grad():
    for i, batch in enumerate(tqdm(test_loader)):
        features = batch
        features = features.to(device)

        outputs = model(features)

        _, test_pred = torch.max(outputs, 1) # 获得概率最高的类的索引
        pred = np.concatenate((pred, test_pred.cpu().numpy()), axis=0)

with open(os.path.join(models_dir, 'prediction.csv'), 'w') as f:
    f.write('Id,Class\n')
    for i, y in enumerate(pred):
        f.write('{},{}\n'.format(i, y))
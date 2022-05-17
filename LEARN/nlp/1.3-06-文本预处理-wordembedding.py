# 导入torch和tensorboard的摘要写入方法
import torch
import json
import fileinput
from tensorboardX import SummaryWriter
# 实例化一个摘要写入对象
writer = SummaryWriter()

# 随机初始化一个100x50的矩阵, 认为它是我们已经得到的词嵌入矩阵
# 代表100个词汇, 每个词汇被表示成50维的向量
embedded = torch.randn(100, 50)

# 导入事先准备好的100个中文词汇文件, 形成meta列表原始词汇
# meta = list(map(lambda x: x.strip(), fileinput.FileInput("./vocab100.csv")))
meta = [str(i) for i in range(100)]
writer.add_embedding(embedded, metadata=meta)
writer.close()

# tensorboard --logdir runs --host 0.0.0.0
# 通过http://0.0.0.0:6006访问浏览器可视化页面，本地调用服务器，要把ip改成服务器ip

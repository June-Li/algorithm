"""
简介：
1. pytorch的两大功能：
    1）numpy的替代者，并且提供了强大的GPU支持；
    2）有许多方便的深度学习运算接口；
2. pytorch的基本元素：
    tensor：类似于numpy的ndarray，但是Tensor可以利用GPU；
"""
import torch
import numpy as np

# 结构生成向量---开始
"""
生成tensor
"""

"""
函数                                  功能
Tensor(*sizes)                       基础构造函数
ones(*sizes)                         全1Tensor
zeros(*sizes)                        全0Tensor
eye(*sizes)                          对角线为1，其他为0
arange(s,e,step)                     从s到e,步长为step
linspace(s,e,steps)                  从s到e,均匀切分成steps份
rand/randn(*sizes)                   均匀/标准分布
normal(mean,std)/uniform(from,to)    正态分布/均匀分布
randperm(m)随机排列
"""
x = torch.empty(5, 3)
print(x)

x = torch.rand(5, 3)
print(x)

x = torch.zeros(5, 3, dtype=torch.long)
print(x)
# 结构生成向量---结束

# 具体定义生成向量---开始
x = torch.tensor([1, 2, 4])
print(x)
# 具体定义生成向量---结束

# 其他方式---开始
x = torch.ones_like(x, dtype=torch.float)  # size和x相同，其他可以指定
print(x)

x = torch.rand_like(x, dtype=torch.float)
print(x)
# 其他方式---结束

# tensor属性--开始
print(x.size())  # 虽然返回假如是torch.Size([5, 3])，像列表，但其实是个tuple，可以用两个变量接，a, b = x.size()
# print(torch.Size)
# Tensor属性---结束

"""
操作tensor
"""
# 切片操作，和numpy一样
x = torch.randn(4, 4)
print(x[:, 1])

# 改变形状
x = torch.randn(4, 4)
y = x.view(16)
z = x.view(-1, 8)
print(x)
print(y)
print(z)

# 如果张量中只有一个元素,可以用.item()将值取出,作为一个python number
x = torch.randn(1)
print(x)
print(x.item())

# tensor和numpy之间的转换，Torch Tensor和Numpy array共享底层的内存空间,因此改变其中-个的值,另一个也会随之被改变.
# tensor转numpy
a = torch.ones(5)
print(a)
b = a.numpy()
print(b)
a.add_(1)
print(a)
print(b)

# numpy转tensor，底层仍然是共享内存空间的
a = np.ones(5)
b = torch.from_numpy(a)
np.add(a, 1, out=a)
print(a)
print(b)

# 加法
x = torch.randn(3)
y = torch.randn(3)
result = torch.randn(3)
x+y
torch.add(x, y)
torch.add(x, y, out=result)
y.add_(x)

# 所有在CPU上的Tensors,除了CharTensor,都可以转换为Numpy array并可以反向转换
# 关于Cuda Tensor: Tensors可以用.to()方法来将其移动到任意设备上，转numpy必须是cpu上。
if torch.cuda.is_available():
    device = torch.device('cuda')
    y = torch.ones_like(x, device=device)
    x = x.to(device)
    z = x + y
    print(z)
    print(z.to('cpu', torch.double))

"""
end
"""
"""
学习目标：
    1.掌握自动求导中的tensor概念和操作；
    2.掌握自动求导中的梯度gradients概念和操作；
简介：
    1.在整个pytorch框架中，所有的神经网络本质上都是一个autograd package（自动求导工具包）
        1）autograd packpage提供了一个对tensor上所有的操作进行自动微分的功能；
    2.torch.Tensor类：
        1) torch.Tensor是整个package中的核心类,如果将属性.requires_grad设置为True,它将追踪在这
        个类上定义的所有操作.当代码要进行反向传播的时候,直接调用backward()就可以自动计算所有的梯度.在
        这个Tensor上的所有梯度将被累加进属性.grad中.
        2) 如果想终止一个Tensor在计算图中的追踪回溯，只需要执行detach()就可以将该Tensor从计算图中撤
        下，在未来的回溯计算中也不会再计算该Tensor,也就是不再进行方向传播求导数的过程，相当于把
        requires_grad设置为False.
        3) 除了.detach(),如果想终止对计算图的回溯，也可以采用代码块的方式with torch.no_grad() 这
        种方式非常适用于对模型进行预测的时候，因为预测阶段不再需要对梯度进行计算.
    3.torch.Function类：
        1）Tensor和Function类是torch的两个核心类，Tensor和Function共同构建了一个完整的类，每一个
        Tensor拥有一个.grad_fn属性，代表引用了哪个具体的Function创建了该Tensor.
        2）如果Tensor是用户自定义的，则grad_fn=None；
"""
import torch

"""
grad_fn和requires_grad
"""
x1 = torch.ones(3, 3)
print(x1)

# requires_grad=True，可以求导，即用backward()不报错
# requires_grad=False，不可以求导，即用backward()报错
x = torch.ones(2, 2, requires_grad=True)
print(x)

# 只要一个头tensor为True，后边的链式计算都是True
a = torch.randn(2, 2, requires_grad=True)
b = a + 2
c = b + b
print(a.requires_grad)
print(b.requires_grad)
print(c.requires_grad)

# 查看以书面方式构建的Tensor
y = x + 2
z = y * 2
print(y)

print(x.grad_fn)
print(y.grad_fn)
print(z.grad_fn)

z = y * y * 3
out = z.mean()
print(z, out)

a = torch.randn(2, 2)
a = ((a*3)/(a-1))
print(a.requires_grad)  # 默认为False
a.requires_grad_(True)  # 末尾带一个下划线的代表就地改变
print(a.requires_grad)
b = (a*a).sum()
print(b)
print(b.grad_fn)  # 输出是SumBackWard，因为tensor构建只跟最后一次操作有关

# detach()，多用with torch.no_grad()，少用detach()
x = torch.randn(2, 2)
y = x.detach()
print(y.requires_grad)
print(x)
print(y)
print(x.eq(y).all())  # eq()只比较值，不比较其他属性

"""
梯度backward()，这是tf和torch最关键的部分
"""
# backward
out.backward()
print(x.grad)  # 获取梯度

"""
end
"""

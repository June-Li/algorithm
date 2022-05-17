"""
简介：
    1.pytorch构建神经网络的主要工具在torch.nn包中；
    2.torch.nn是依赖autogard来构建定义模型，实现前向和后向传播:
        1）nn.xxx和nn.Functional.xxx的区别：
            · nn.xxx是进行了类封装，需要实例化，nn.Functional.xxx是函数，不需要实例化；
            · nn.xxx是类的封装（即nn.Funtional.xxx的封装）并且nn.xxx都继承自共同的父类nn.Module，所以nn.xxx除了有nn.Funtional.xxx
              的功能之外还附带了nn.Module相关的属性和方法，比如，train()、eval()、load_state_dict()、stat_dict()；
            · nn.xxx功能齐全，不需要手动维护weights、bias等（均自动生成），但是需要实例化，不够灵活；
            · nn.Funtional.xxx需要手动维护一些功能（需手动生成weights、bias等），但是比较灵活；
        2）官方推荐：
            有参数训练的层用nn.xxx，没有参数训练的层用nn.Funtional.xxx；
    tips：
        1）dropout使用nn.xxx，因为nn.Funtional.xxx的dropout在eval阶段不会关闭；
    3.构建神经网络的典型流程为：
        2）准备数据：构建好数据迭代器；
        3）网络定义：数据按batch输入网络，网络输出结果；
        4）定义损失：用网络的输出和label计算输出；
        5）定义优化：用什么样的方式优化loss；
        6）计算梯度：对loss进行反向传播，计算梯度；
        7）参数更新：用计算得到的梯度对网络参数进行更新；

学习目标：
    1.用pytorch构建一个神经网络：
        1）损失函数
        2）反向传播
        3）更新网络参数
    2.用pytorch构建一个图片分类器：
        1）分类器任务和数据介绍
        2）训练分类器的步骤
        3）在GPU上训练模型
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim


class Net(nn.Module):
    def __init__(self):
        super().__init__()
        # 定义层，其实就是定义层的参数（可更新变量）
        self.conv1 = nn.Conv2d(1, 6, 3)
        self.conv2 = nn.Conv2d(6, 16, 3)
        self.fc1 = nn.Linear(16*6*6, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        x = F.max_pool2d(F.relu(self.conv1(x)), (2, 2))
        x = F.max_pool2d(F.relu(self.conv2(x)), 2)
        x = x.view(-1, self.num_flat_features(x))
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

    def num_flat_features(self, x):
        size = x.size()[1:]
        num_features = 1
        for s in size:
            num_features *= s
        return num_features


net = Net()
print(net)
params = list(net.parameters())  # 获取参数，并转换成列表
print(len(params))  # 输出有多少个tensor
print(params[0].size())

Input = torch.randn(1, 1, 32, 32)
out = net(Input)
print(out)

targt = torch.randn(10)
targt = targt.view(1, -1)
loss = nn.MSELoss()(out, targt)
print(loss)

# 可以打印出运算链条
print(loss.grad_fn)
print(loss.grad_fn.next_functions[0][0])
print(loss.grad_fn.next_functions[0][0].next_functions[0][0])

# 在执行反向传播之前,要先将梯度清零,否则梯度会在不同的批次数据之间被累加.
# 优化
optimizer = optim.SGD(net.parameters(), lr=0.01)
optimizer.zero_grad()  # ==net.zero_grad()
loss.backward()
optimizer.step()

"""
end
"""
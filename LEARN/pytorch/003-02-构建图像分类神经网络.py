"""
简介：
    1.CIFAR10数据集：
        1）
    2.
学习目标：
    1.了解分类器的任务和数据样式；
    2.使用pytorch实现图像分类器；
"""
import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt


batch = 128
print_num = 1
transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
trainset = torchvision.datasets.CIFAR10(root='./data', train=True, download=True, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch, shuffle=True, num_workers=8)

testset = torchvision.datasets.CIFAR10(root='./data', train=False, download=True, transform=transform)
testloader = torch.utils.data.DataLoader(testset, batch_size=batch, shuffle=False, num_workers=8)

classes = ('plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck')

# 显示示例图片---开始
# def imshow(img):
#     img = img / 2 + 0.5
#     npimg = img.numpy()
#     plt.imshow(np.transpose(np.img, 1, 2, 0))
#     plt.show()
#
#
# dataiter = iter(trainloader)
# images, labels = dataiter.next()
# imshow(torchvision.utils.make_grid(images))
# print(' '.join('%5s' % classes[labels[j]] for j in range(batch)))
# 显示示例图片---结束


class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16*5*5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 16*5*5)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x


net = Net()
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
# device = 'cpu'
net.to(device)
print(net)


# train---开始
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)

for epoch in range(20):
    running_loss = 0.0
    for i, data in enumerate(trainloader):
        inputs, labels = data[0].to(device), data[1].to(device)
        optimizer.zero_grad()
        outputs = net(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        if (i+1) % print_num == 0:
            torch.save(net.state_dict(), './weights/last.pt')  # 这个是只保存可训练参数
            print('[%d, %5d] loss: %.3f' % (epoch + 1, i + 1, running_loss/print_num))
            running_loss = 0.0
# train---结束

# test---开始
# net.load_state_dict(torch.load('./weights/last.pt'))
# correct = 0
# class_correct = [0. for i in range(10)]
# total = 0
# class_total = [0. for i in range(10)]
# with torch.no_grad():
#     for data in testloader:
#         images, labels = data[0].to(device), data[1].to(device)
#         outputs = net(images)
#         _, predicted = torch.max(outputs.data, 1)
#         total += labels.size(0)
#         correct += (predicted == labels).sum().item()
#         c = (predicted == labels).squeeze()
#         for i in range(len(images)):
#             label = labels[i]
#             class_correct[label] += c[i].item()
#             class_total[label] += 1
# print('arr: ', 100*correct/total)
# for i in range(10):
#     print('acc of %5s : %2d %%' % (classes[i], 100 * class_correct[i] /class_total[i]))

# test---结束

"""
end：为啥不能debug
"""
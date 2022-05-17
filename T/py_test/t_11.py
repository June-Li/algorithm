import torch

# aa = torch.ones(2, 2, requires_grad=True)
# print(id(aa))
# print(aa)
# a = aa + 1
# print(id(a))
# print(a)
# a = a + 2
# print(id(a))
# print(a)
# a = a + 3
# print(id(a))
# print(a)
# a = a + 4
# print(id(a))
# print(a)
# a = a + 5
# print(id(a))
# print(a)
# print(aa)
# # a = a + a
# # print(id(a))
# print(a.requires_grad)
# print(b.requires_grad)
# print(c.requires_grad)
# d.backward()

# a = torch.tensor(1., requires_grad=True)
# with torch.no_grad():
#     # b = torch.add(a, a)
#     b = a + a
# bb = (a + a)
# print(bb)
# b = bb.detach()
# b += 2
# print(bb)
# print(b)
# print(id(b))
# print(b.grad_fn)
# print(id(b))
# # c = torch.add(b, b)
#
# c = b + b
# print(c.requires_grad)
# c.requires_grad_(True)
# print(c.requires_grad)
# # a = a.mean()
# # print(a.type())
# # print(a)
# #
# # a = torch.ones(2, 2, requires_grad=True)
# # print(a.type())
# c.backward()
# print(b.grad)
# print(c.grad)


# a = torch.ones(2, 2, requires_grad=True)
# b = a * 3
# # with torch.no_grad():
# #     c = b * 2
# c = b * 2
# d = c * 2
# # d.requires_grad_(True)
# e = d.mean()
# e.backward()
#
# print(a.grad)
# print(b.grad)
# print(c.grad)
# print(d.grad)
# print(e.grad)

a = torch.ones(2, 2, requires_grad=True)
b = a * torch.Tensor(2, 2)
c = b.mean()
c.backward()
print(c.grad)

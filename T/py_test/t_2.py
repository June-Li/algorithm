class dataloader:
    def __init__(self):
        pass

    def __len__(self):
        pass

    def __getitem__(self, item):
        return item


data = dataloader()
for i in range(99):
    print(data[i])

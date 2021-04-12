# 方法一：
base_path = '/Volumes/my_disk/company/sensedeal/dataset/生成的中文数据/char_std_5990.txt'
with open(base_path, 'rb') as file:
    char_dict = {num: char.strip().decode('gbk', 'ignore') for num, char in enumerate(file.readlines())}
print(char_dict)

# 方法二：
base_path = '/Volumes/my_disk/company/sensedeal/dataset/生成的中文数据/char_std_5990.txt'
file = open(base_path, "r", encoding="latin1").readlines()

count = 0
chn_list = []
for line in file:
    count += 1
    line_chn = line.encode('latin1').decode('GB18030').rstrip('\n')
    chn_list.append(line_chn)
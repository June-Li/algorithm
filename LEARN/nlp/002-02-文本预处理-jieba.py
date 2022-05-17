"""
介绍：
    jieba是优秀的中文分词器（Tokenizer）第三方库
常用函数：
    jieba.cut(s)                    精确模式,返回-个可迭代的数据类型
    jieba.cut(s, cut_all=True)      全模式,输出文本s中所有可能单词
    jieba.cut_for_search(s)         搜索引擎模式，适合搜索引擎建立索引的分词结果
    jieba.lcut(s)                   精确模式，返回一个列表类型，建议使用
    jieba.lcut(s, cut_all=True)     全模式，返回一-个列表类型，建议使用
    jieba.lcut_for_search(s)        搜索引擎模式，返回一个列表类型,建议使用
    jieba.add_word(w)               向分词词典中增加新词w
    jieba.load_userdict(file)       添加新的词典
"""
import jieba

content = '我叫李俊，你叫什么名字啊，我是一个程序员，你呢'

# 精确模式分词：试图将句子最精确地切开，适合文本分析.
cut_out = jieba.cut(content, cut_all=False)
for s in cut_out:
    print(s)
cut_out_list = jieba.lcut(content, cut_all=False)
# ['我', '叫', '李俊', '，', '你', '叫', '什么', '名字', '啊', '，', '我', '是', '一个', '程序员', '，', '你', '呢']
print(cut_out_list)

# 全模式分词：把句子中所有的可以成词的词语都扫描出来,速度非常快，但是不能消除歧义.
cut_out = jieba.lcut(content, cut_all=True)
# ['我', '叫', '李俊', '，', '你', '叫', '什么', '名字', '啊', '，', '我', '是', '一个', '一个程', '程序', '程序员', '，', '你', '呢']
print(cut_out)

# 搜索引擎模式分词：在精确模式的基础上，对长词再次切分，提高召回率，适合用于搜索引擎分词.
cut_out_search = jieba.lcut_for_search(content)
# ['我', '叫', '李俊', '，', '你', '叫', '什么', '名字', '啊', '，', '我', '是', '一个', '程序', '程序员', '，', '你', '呢']
print(cut_out_search)

# 中文繁体分词：针对中国香港,台湾地区的繁体文本进行分词.
content = '煩惱即是菩提，我暫且不提'
cut_out_f = jieba.lcut(content)
print(cut_out_f)

"""
jieba可以使用用户自定义词典:
    ●添加自定义词典后, jieba能够准确识别词典中出现的词汇，提升整体的识别准确率.
    ●词典格式:每一行分三部分:词语、词频(可省略)、 词性(可省略) ，用空格隔开,顺序不可颠倒.
    ●词典样式如下,具体词性含义请参照附录: jieba词性对照表,将该词典存为userdict.txt,方便之后加载使用.
    
    丢计算 5 n
    李小福 2 nr
    easy-install 3 eng
    好用 300
    韩玉赏鉴3  nz
    八一双鹿 3 nz

用法：
    jieba.load_userdict()，load后会与jieba原先的词典组合起来。
"""
content = '我是一个程序员，八一南昌'
cut_out = jieba.lcut(content)
print(cut_out)
jieba.add_word('八一南昌')
# jieba.load_userdict('./utils/jieba_dict.txt')
cut_out = jieba.lcut(content)
print(cut_out)

# # 举例：利用jieba库统计三国演义中任务的出场次数
txt = open("D:\\三国演义.txt", "r", encoding='utf-8').read()
words = jieba.lcut(txt)  # 使用精确模式对文本进行分词
counts = {}  # 通过键值对的形式存储词语及其出现的次数

for word in words:
    if len(word) == 1:  # 单个词语不计算在内
        continue
    else:
        counts[word] = counts.get(word, 0) + 1  # 遍历所有词语，每出现一次其对应的值加 1

items = list(counts.items())  # 将键值对转换成列表
items.sort(key=lambda x: x[1], reverse=True)  # 根据词语出现的次数进行从大到小排序

for i in range(15):
    word, count = items[i]
    print("{0:<5}{1:>5}".format(word, count))

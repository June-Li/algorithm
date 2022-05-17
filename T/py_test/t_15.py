# 一般n-gram中的n取2或者3, 这里取2为例
ngram_range = 2

#
# def create_ngram_set(input_list):
#     # return set(zip(*[input_list[i:] for i in range(ngram_range)]))
#     return zip(*[input_list[i:] for i in range(ngram_range)])
#
#
# input_list = [1, 3, 2, 1, 5, 3]
# res = create_ngram_set(input_list)
# print(res)
# for i in res:
#     print(i)

a = set(zip(*[[1, 2, 3], [40, 5, 6, 7]]))
print(a)

"""
并查集有两个优化方式，路径压缩和秩压缩。
"""


class DisjointSet():
    def __init__(self, edges):
        self.edges = edges
        self.point_set = set()
        for edge in self.edges:
            self.point_set.add(edge.split('&')[0])
            self.point_set.add(edge.split('&')[1])
        self.parent = {i: i for i in self.point_set}
        self.rank = {i: 0 for i in self.point_set}

    # 并
    def union(self, pt_1, pt_2):
        pt_1_parent, pt_2_parent = self.find(pt_1), self.find(pt_2)
        if self.rank[pt_1_parent] > self.rank[pt_2_parent]:
            self.parent[pt_2_parent] = pt_1_parent
        elif self.rank[pt_1_parent] < self.rank[pt_2_parent]:
            self.parent[pt_1_parent] = pt_2_parent
        else:
            self.rank[pt_1_parent] += 1
            self.parent[pt_2_parent] = pt_1_parent

    # 查
    def find(self, pt):
        if self.parent[pt] != pt:
            self.parent[pt] = self.find(self.parent[pt])  # 路径压缩
        return self.parent[pt]

    # 集
    def __call__(self, *args, **kwargs):
        for edge in self.edges:
            self.union(edge.split('&')[0], edge.split('&')[1])
        self.connected_domain_num = sum(self.parent[i] == i for i in self.parent)
        return self.parent, self.connected_domain_num


if __name__ == '__main__':
    # edges = ['AB', 'AC', 'AD', 'IL', 'MK', 'IM', 'IJ', 'ED', 'HG', 'HF', 'BG', 'DI']
    # edges = ['A&B', 'C&D', 'B&D']
    # edges = ['A&B', 'B&C', 'C&D']
    edges = ['11&12', '12&13', '13&14']
    alg_object = DisjointSet(edges)
    print(alg_object())

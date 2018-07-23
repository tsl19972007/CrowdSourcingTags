from math import sqrt
from sys import argv

prefix = argv[1]

with open(prefix + '/param.txt', 'r') as fr:
    n_user = int(fr.readline())
    n_task = int(fr.readline())
    k = int(fr.readline())
    Y = [[0] * n_task] * n_user
    for i in range(n_user):
        Y[i] = fr.readline().split(" ")
        for j in range(n_task):
            Y[i][j] = float(Y[i][j])
    ratings = fr.readline().split(" ")
    for j in range(n_task):
        ratings[j] = float(ratings[j])

# 计算pearson距离
def pearson(rating1, rating2):
    sum_xy = 0
    sum_x2 = 0
    sum_y2 = 0
    sum_x = 0
    sum_y = 0
    n = 0
    for i in range(len(rating1)):
        if rating1[i] > 0 and rating2[i] > 0:
            n += 1
            sum_xy += rating1[i] * rating2[i]
            sum_x2 += rating1[i] * rating1[i]
            sum_y2 += rating2[i] * rating2[i]
            sum_x += rating1[i]
            sum_y += rating2[i]
    if n == 0:
        return 0
    else:
        sx = sqrt(sum_x2 - pow(sum_x, 2)/n)
        sy = sqrt(sum_y2 - pow(sum_y, 2)/n)
        if sx != 0 and sy != 0:
            return (sum_xy - sum_x*sum_y/n) / sx / sy
        else:
            return 0
# 计算每个人与待推荐用户的pearson距离
distances = []
for i in range(len(Y)):
    distance = pearson(Y[i], ratings)
    distances.append(distance)
index = distances.index(max(distances))
# 把和待推荐用户pearson距离最大的人作为推荐样本
rating_list = []
for j in range(len(Y[0])):
    rating_list.append((min(Y[index][j], ratings[j]), j))
# 排序之后选评分前k高的
rating_list = sorted(rating_list, key=(lambda x: x[0]), reverse=True)

with open(prefix + '/result.txt', 'w') as fw:
    for i in range(k):
        fw.write(str(rating_list[i][1]) + '\n')

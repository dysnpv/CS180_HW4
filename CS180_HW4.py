import random

infty = 2**20

# This is my solution.
def Q2_my_algorithm(n, K, x):
    c = [[infty for i in range(K + 1)] for j in range(n + 1)]
    p = [[[0 for i in range(K + 1)] for j in range(K + 1)] for k in range(n + 1)]
    d = [[0 for i in range(n + 1)] for j in range(n + 1)]
    c[0][0] = c[1][1] = 0
    p[1][1][1] = 1
    for i in range(1, n + 1):
        d[i][i] = 0
        for j in range(i + 1, n + 1):
            # There was a minor error in my solution. It should be "(i + j)/2" instead of "(i + j + 1)/2".
            d[i][j] = d[i][j - 1] + x[j] - x[int((i + j)/2)]
    for i in range(2, n + 1):
        for j in range(1, min(i, K) + 1):
            s = -1
            for t in range(1, i + 1):
                if d[t][i] + c[t - 1][j - 1] < c[i][j]:
                    c[i][j] = d[t][i] + c[t - 1][j - 1]
                    s = t
            for t in range(1, j):
                p[i][j][t] = p[s - 1][j - 1][t]
            p[i][j][j] = int((s + i + 1)/2)
    return c[n][K], p[n][K]

# This is the solution given to the class.
def Q2_solution(n, K, x):
    cost = [[infty for i in range(n + 1)] for j in range(n + 1)]
    L = [[infty for i in range(K + 1)] for j in range(n + 1)]
    for p in range(1, n):
        c = p
        cost[p][p + 1] = 0
        for i in range(p + 2, n + 1):
            cost[p][i] = cost[p][i - 1] + (i - 1 - c) * (x[i] - x[i - 1])
            while(c + 1 < i and abs(x[p] - x[c + 1]) <= abs(x[i] - x[c + 1])):
                c += 1
                cost[p][i] -= abs(x[i] - x[c]) - abs(x[p] - x[c])
    for i in range(1, n + 1):
        s = 0
        for j in range(1, i):
            s += abs(x[i] - x[j])
        L[i][1] = s
        for j in range(1, K + 1):
            for p in range(j - 1, i):
                if L[i][j] > L[p][j - 1] + cost[p][i]:
                    L[i][j] = L[p][j - 1] + cost[p][i]
    min_L = infty
    for i in range(1, n + 1):
        s = 0
        for j in range(i + 1, n + 1):
            s += abs(x[i] - x[j])
        if min_L > L[i][K] + s:
            min_L = L[i][K] + s
    return min_L

# Run this function to verify my solution returns the correct answer.
def verification():
    cnt = 5
    for t in range(cnt):
        n = random.randint(5, 200)
        for K in range(1, int(n/2)):
            x = [infty]
            randlist = random.sample(range(10000), n)
            randlist.sort()
            x = x + randlist
            cost1, placement1 = Q2_my_algorithm(n, K, x)
            cost2 = Q2_solution(n, K, x)
            # Verify that both algorithms give the same cost
            assert(cost1 == cost2)
            # Verify that my algorithm's cost is valid. That is, the cost can be obtained by placing the fire stations by the given way.
            s = 0
            p = 1
            for i in range(1, n + 1):
                if p == K:
                    s += abs(x[i] - x[placement1[p]])
                else:
                    if abs(x[i] - x[placement1[p]]) > abs(x[i] - x[placement1[p + 1]]):
                        s += abs(x[i] - x[placement1[p + 1]])
                        p += 1
                    else:
                        s += abs(x[i] - x[placement1[p]])
            assert(s == cost1)
    print("Verification done.")
N = int(input())
A = list(map(int, input().split()))

count = [0] * N
for x in A:
    count[x - 1] += 1

print(count.index(3) + 1)

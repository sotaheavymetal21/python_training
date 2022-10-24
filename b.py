N = int(input())
H = list(map(int, input().split()))

volcano = H[-1]

for i in range(N - 1):
    if H[i] > H[i + 1] or H[i] == H[i + 1]:
        volcano = H[i]
        print(volcano)
        exit()
print(volcano)

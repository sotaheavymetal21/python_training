N, Q = map(int, input().split())
A = list(map(int, input().split()))
xy = [map(int, input().split()) for _ in range(Q)]
x, y = [list(i) for i in zip(*xy)]
print(N, Q, A, x, y)

for i in range(Q):
    for j in range(N):
        if x[i] == A[j]:
            print(A[j])
            A.pop(A[j])
        else:
            print(-1)

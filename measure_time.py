import time

# 開始
start_time = time.perf_counter()

A = 1000

count = 0
for i in range(A):
    for j in range(A):
        for k in range(A):
            count += 1

# 修了
end_time = time.perf_counter()

# 経過時間を出力(秒)
elapsed_time = end_time - start_time
print(elapsed_time)

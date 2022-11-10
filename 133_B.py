# 標準入力
N, D = map(int, input().split())
# 複数行の標準入力
X = [list(map(int, input().split())) for _ in range(N)]

# 座標の距離が整数である場合はこのカウンターを＋１する
# 何かの数をカウントする場合は最初にカウンターを０で定義しておくとよい
counter = 0

# ひとつひとつ調べていく探索なのでループ文を用いる
# 比較したい行を選択する
# N個の点があるのでrangeはNで回す
for i in range(N):
    # iと比較する行を別に指定するので、rangeはi + 1としている（iとは被らないようにする）
    for j in range(i + 1, N):
        # kのfor文が終了し、jの値が変わる時、distanceの値が引き継がれないように0で再定義
        distance = 0
        # rangeは次元数を指定する
        for k in range(D):
            # 距離（distance）を調べる
            # 二次元配列
            # iとjは据え置き（比較する行は変わらないから）
            # ２次元以上だと何回か計算する必要があるので+=として計算するたびに加算されるようにする
            distance += (X[i][k] - X[j][k]) ** 2
        # math.sqrt()で平方根をかけるか、0.5をかけると正確な距離が出る
        # それが整数であるか判断をする
        if  (distance **0.5).is_integer():
            # 整数であればカウンターが＋１される
            counter += 1

# カウンターを出力
print(counter)

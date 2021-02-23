n = int(input())
for i in range(2, n):
    p = True
    for j in range(2, i):
        if i % j == 0:
            p = False
    if p:
        print(i)
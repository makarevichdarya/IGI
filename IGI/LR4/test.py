import math

s = list(map(int, input().split()))

s_l = 0
for i in s:
    s_l *= i

max1 = max(s)
s.remove(max1)
max2 = max(s)
print(max1, max2)

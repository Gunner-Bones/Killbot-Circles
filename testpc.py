l1 = [2,45,6,1,78]
l2 = [23,1,45]
l = True
for t2 in l2:
    if not l: break
    for t1 in l1:
        if t1 == t2:
            l = True
            break
        l = False
print(l)
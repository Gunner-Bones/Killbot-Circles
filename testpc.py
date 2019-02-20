def samelists(l1,l2):
    if len(l1) == 0 or len(l2) == 0: return False
    if len(l1) == 1 and len(l2) == 1 and l1[0] == l2[0]: return True
    lv = 0; lu = []
    for d1 in l1:
        for d2 in l2:
            if d2 == d1 and d1 not in lu:
                lv += 1; lu.append(d1); break
    if lv == len(l1) and lv == len(l2): return True
    return False

def differencesinlists(l1,l2):
    if samelists(l1,l2): return []
    dil = []
    for d1 in l1:
        if d1 not in l2 and d1 not in dil: dil.append(d1)
    for d2 in l2:
        if d2 not in l1 and d2 not in dil: dil.append(d2)
    return dil

test1 = ["finale","pulse","plasma","j","dd"]
test2 = ["plasma","pulse","finale","j"]
print(differencesinlists(test1,test2))

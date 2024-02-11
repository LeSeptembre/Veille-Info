def lexing1(var):
    tokken = ["Montrer"]
    s1 = list(var)

    i = 0
    while i < len(s1) - 2:
        if s1[i].isdigit() and  s1[i + 1]=="." and s1[i + 2].isdigit():
            k = i+2
            while s1[k].isdigit():
                k+=1
            s1[i] = "".join(s1[i:k])
            del s1[i + 1: k]
            i+=1

        else:
            i+=1

    for k in tokken:
        indexs1 = 0
        while indexs1 < len(s1):
            if k.endswith(s1[indexs1]) and indexs1 + 1 >= len(k):
                flag = all(k[e - 1] == s1[indexs1 - (len(k) - e)] for e in range(len(k), 0, -1))
                if flag:
                    s1[indexs1] = "".join(s1[indexs1 - len(k) + 1: indexs1 + 1])
                    del s1[indexs1 - len(k) + 1: indexs1]
                    indexs1 = 0
            indexs1 += 1

    indexs1 = 0
    while indexs1 < len(s1) - 1:
        if s1[indexs1] == '"':
            index0 = indexs1 + 1
            while s1[index0] != '"':
                index0 += 1
            s1[indexs1] = "".join(s1[indexs1: index0 + 1])
            del s1[indexs1 + 1: index0 + 1]
            indexs1 += 1

        indexs1 += 1

    for ins in reversed(s1):
        if ins == " ":
            s1.remove(ins)

    return s1


var = 'Montrer :  3+5.22545.'
print(lexing1(var))

def antena(lista):
    lmax = max(lista)
    ant = []
    j = 0
    for i in range(lmax):
        print j
        if j >= lmax:
            if j - ant[-1] <= 4:
                return ant
        if j in lista:
            j += 4
            ant.append(j)
            j += 4
        else:
            j += 1
    return ant


print antena([3, 16, 11, 18, 5, 17, 24, 29, 1, 301])

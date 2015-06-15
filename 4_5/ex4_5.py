def antena(lista):
    #lista = lista
    lmax = max(lista)
    #k = k
    ant = []
    j = 0
    for i in range(lmax):
        #import pdb; pdb.set_trace()
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


print antena([3, 16, 11, 18, 5, 17, 24, 29, 1])

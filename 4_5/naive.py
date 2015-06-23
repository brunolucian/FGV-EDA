def antena(lista):
    lmax = max(lista)
    ant = []
    j = 0
    for i in range(lmax):
        if j >= lmax:
            return ant
        j += 4
        ant.append(j)


print antena([3, 16, 11, 18, 5, 17, 24, 29, 1, 301])

def antena2(lista):
    ant=[]
    for i in lista:
        ant.append(lista[lista.index(i)])

    ant.sort()
    return ant

print antena2([3, 16, 11, 18, 5, 17, 24, 29, 1, 301])
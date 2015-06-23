def restaurante(distancias,k,lucros):
    
    lmax = max(distancias)
    rest = []
    lucro = []
    lucro.append(0)
    j = 0
    for i in range(lmax):
        if j in distancias:
            rest.append(distancias[distancias.index(j)])
            lucro.append(lucros[distancias.index(j)])
            j=j+k
        else:
            j += 1
    return sum(lucro)


print restaurante([3, 8, 9, 15],3,[5, 6, 10, 8])
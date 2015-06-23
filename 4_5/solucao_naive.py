
def antena(lista):
    lmax = max(lista) # Valor maximo presente na lista de distancias
    ant = []
    j = 0
    for i in range(lmax): # Coloca uma antena a cada 4 milhas
        if j >= lmax: # Ver se a antena tem posicao maior que maximo da lista
            return ant
        j += 4
        ant.append(j)
print antena([3, 16, 11, 18, 5, 17, 24, 29, 1, 301])
print antena([3, 16, 11, 18, 5, 17, 24, 29, 1, 301])
print antena([3, 16, 11, 18, 5, 17, 24, 29, 1, 301])
print antena([3, 16, 11, 18, 5, 17, 24, 29, 1, 301])

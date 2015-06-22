import math
import numpy as np
def antena(lista):

    lmax = max(lista)
    ant = []
    while lista != []: # Realizar procedimento até lista estar vazia, ou seja todas as casas cobertas
        torre = np.random.randint(1, lmax) #fixando uma torre em um ponto qualquer
        #for i in range(len(lista)): 
        for j in lista: #Percorrendo toda a lista
             if j >= torre-4 and j <= torre+4: # Verifica se tem casa está coberta pela torre
                 lista.remove(j) # remove a casa coberta
                 ant.append(torre) # adciona a torre a lista

    ant = list(set(ant)) # Remove as torres colocadas em duplicatas
    ant.sort() #Ordena as torres

    return ant


print antena([3, 16, 11, 18, 5, 17, 24, 29, 1, 301])

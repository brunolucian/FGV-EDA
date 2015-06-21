import math
import numpy as np
def antena(lista):

    lmax = max(lista)
    ant = []
    while lista != []: # Realizar procedimento até lista estar vazia, ou seja todas as casas cobertas
        torre = np.random.randint(1, lmax) #fixando uma torre em um ponto qualquer
        for i in range(len(lista)): #Percorrendo toda a lista
          for i in lista: # 
              if i >= torre-4 and i <= torre+4: # Verifica se tem casa está coberta pela torre
                  lista.remove(i) # remove a casa coberta
                  ant.append(torre) # adciona a torre a lista

    ant = list(set(ant)) # Remove as torres colocadas em duplicatas
    ant.sort() #Ordena as torres

    return ant


print antena([3, 6, 11, 18, 17, 1, 24, 32, 53, 2, 74, 91, 201, 4, 66])

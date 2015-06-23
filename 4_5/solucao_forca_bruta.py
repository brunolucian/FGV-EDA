
import math, numpy
def antena(lista):
  lmax = max(lista)# Valor maximo presente na lista de distancias
  ant = []

  while lista != []: # Realizar procedimento ate todas as casas cobertas
      torre = numpy.random.randint(1, lmax) #fixando uma torre em um ponto qualquer
      for j in lista: #Passando toda a lista
          if j >= torre-4 and j <= torre+4: # Verifica se tem casa esta coberta
              lista.remove(j) # remove a casa coberta
              ant.append(torre) # adciona a torre a lista

  ant = list(set(ant)) # Remove as torres colocadas em duplicatas
  ant.sort() #Ordena as torres

  return ant
print antena([3, 16, 11, 18, 5, 17, 24, 29, 1, 301])
print antena([3, 16, 11, 18, 5, 17, 24, 29, 1, 301])
print antena([3, 16, 11, 18, 5, 17, 24, 29, 1, 301])
print antena([3, 16, 11, 18, 5, 17, 24, 29, 1, 301])

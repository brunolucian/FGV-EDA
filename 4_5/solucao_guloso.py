
def antena(lista):
    ant = []
    lista.sort()

    tamanho = len(lista)
    for i in range(tamanho):
        if len(ant) == 0:
            # O valor de -10 nao afeta a resposta, pois as posicoes
            # das casas sao positivas
            alcance = -10
        else:
            alcance = ant[-1] + 4

        if lista[i] > alcance:
            ant.append(lista[i] + 4)

    return ant
print antena([3, 16, 11, 18, 5, 17, 24, 29, 1, 301])

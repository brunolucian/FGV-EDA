
def restaurante(distancias, k, lucros):
    distancia_possivel = 0
    lucro = 0

    # Percorrendo toda a QVH
    for i in range(len(distancias)):
        if distancias[i] >= distancia_possivel:
            lucro += lucros[i]
            distancia_possivel = distancias[i] + k

    return lucro
print restaurante([3, 8, 9, 15], 3, [5, 6, 10, 8])

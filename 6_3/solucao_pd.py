
def calcula_i_dispo(distancias, k):
    i_dispo = []
    k_milhas_para_tras = -1

    for i in xrange(len(distancias)):
        while distancias[k_milhas_para_tras + 1] <= distancias[i] - k:
            k_milhas_para_tras += 1
        i_dispo.append(k_milhas_para_tras)

    return i_dispo
def restaurante(distancias, k, valores):
    i_dispo = calcula_i_dispo(distancias, k)

    # Iniciando vetor de zeros de tamanho n+1
    lucros = [0 for _ in range(len(valores) + 1)]

    for i in range(len(distancias)):
        # Calculando L(i_dispo)
        d_novo = lucros[i_dispo[i] + 1]

        # Calculando o lucro acumulado da posicao i
        lucros[i + 1] = max(lucros[i], valores[i] + d_novo)

    return lucros[-1] # retorna o maior lucro calculado
print restaurante([3, 8, 9, 15], 3, [5, 6, 10, 8])

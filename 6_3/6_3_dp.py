def restaurante(distancias,k,pay):
    lucro = [0 for a in range(len(pay)+1)]
    for i in range(len(distancias)):
        m_novo = distancias[i]-k
        i_est=[b for b in distancias if b <= m_novo]
        if len(i_est) > 0:
            i_est=i_est[-1]
            d_est= distancias.index(i_est)
            d_novo=lucro[d_est+1]
        else:
            d_novo=0
        lucro[i+1]=max(lucro[i],pay[i]+d_novo)

    return lucro[-1]

print restaurante([3, 8, 9, 15],3,[5, 6, 10, 8])
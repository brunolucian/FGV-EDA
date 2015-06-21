
seguros=[["Vasilhame", "Cam. seguros"], [1, "1, 4"], [2, "1, 2"], [3, "3, 4"], [4, 4], [5, "1, 2, 3, 4"], [6, 1], [7, 3], [8, "1, 2, 3"], [9, "2, 3"], [10, 4]]
regras=[["Capacidade", 3], ["Total de cam.", 4], ["Total de vas.", 10]]
# coding: utf-8
import collections

class Aresta():
    def __init__(self, origem, destino, capacidade, demanda):
        self.origem = origem
        self.destino = destino
        self.capacidade = capacidade
        self.demanda = demanda
        self.reversa = None
        self.original = True

class RedeDeFluxo():
    def __init__(self):
        self.adj = collections.OrderedDict()
        self.fluxo = {}

    def novo_vertice(self, v):
        self.adj[v] = []

    def nova_aresta(self, origem, destino, capacidade, demanda):
        aresta = Aresta(origem, destino, capacidade, demanda)
        self.adj[origem].append(aresta)

        # Criando a aresta reversa
        aresta_reversa = Aresta(destino, origem, 0, -demanda)
        self.adj[destino].append(aresta_reversa)
        aresta_reversa.original = False

        # Marcando aresta e aresta_reversa como reversas uma da outra
        aresta.reversa = aresta_reversa
        aresta_reversa.reversa = aresta

    def novo_fluxo(self, e, f):
        self.fluxo[e] = f

    def encontra_arestas(self, v):
        return self.adj[v]

    def valor_do_fluxo(self, fonte):
        valor = 0
        for aresta in self.encontra_arestas(fonte):
            valor += self.fluxo[aresta]
        return valor

    def encontra_gargalo(self, caminho):
        residuos = []
        for aresta in caminho:
            residuos.append(aresta.capacidade - self.fluxo[aresta])
        return min(residuos)

    def expande_caminho(self, caminho):
        gargalo = self.encontra_gargalo(caminho)
        for aresta in caminho:
            self.fluxo[aresta] += gargalo
            self.fluxo[aresta.reversa] -= gargalo

    def cria_fluxo_inicial(self):
        for vertice, arestas in self.adj.iteritems():
            for aresta in arestas:
                self.fluxo[aresta] = 0

    def encontra_caminho(self, fonte, dreno, caminho, visitados):
        if fonte == dreno:
            return caminho

        visitados.add(fonte)

        for aresta in self.encontra_arestas(fonte):
            residuo = aresta.capacidade - self.fluxo[aresta]
            if residuo > 0 and aresta.destino not in visitados:
                resp = self.encontra_caminho(aresta.destino,
                                             dreno,
                                             caminho + [aresta],
                                             visitados)
                if resp != None:
                    return resp

    def fluxo_maximo(self, fonte, dreno):
        self.cria_fluxo_inicial()

        caminho = self.encontra_caminho(fonte, dreno, [], set())
        while caminho is not None:
            self.expande_caminho(caminho)
            caminho = self.encontra_caminho(fonte, dreno, [], set())
        return self.valor_do_fluxo(fonte)


capacidade_por_caminhao = regras[0][1]
total_de_vasilhames = regras[2][1]

vasilhames = collections.OrderedDict()
caminhoes = []
for line in seguros[1:]:
    # Nomeando os vasilhames
    vasilhame = 'v_%s' % line[0]
    vasilhames[vasilhame] = []
    for caminhao in str(line[1]).split(','):
        nome = 'C_%s' % caminhao.strip()
        vasilhames[vasilhame].append(nome)
        if nome not in caminhoes:
            caminhoes.append(nome)

def cria_grafo(vasilhames, caminhoes, capacidade_por_caminhao):
    G = RedeDeFluxo()
    G.novo_vertice('Fonte')
    G.novo_vertice('Dreno')

    # Criando um vertice para cada caminhao e ligando esse
    # vertice ao dreno
    for caminhao in caminhoes:
        G.novo_vertice(caminhao)
        G.nova_aresta(caminhao, 'Dreno',
                      capacidade_por_caminhao, 0)

    for vasilhame, caminhoes in vasilhames.iteritems():
        # Criando um vertice para cada vasilhame e conectando
        # a fonte a cada um dos vasilhames
        G.novo_vertice(vasilhame)
        G.nova_aresta('Fonte', vasilhame, 1, 0)

        # Conectando o vasilhame a cada caminhao que pode
        # transporta-lo
        for caminhao in caminhoes:
            G.nova_aresta(vasilhame, caminhao, 1, 0)

    return G

G = cria_grafo(vasilhames, caminhoes, capacidade_por_caminhao)
fluxo = G.fluxo_maximo('Fonte', 'Dreno')
if fluxo == total_de_vasilhames:
    tabela_de_vasilhames = []
    for vasilhame in vasilhames:
        for w in G.adj[vasilhame]:
            if G.fluxo[w] == 1:
                tabela_de_vasilhames.append([w.origem, w.destino])
    print tabela_de_vasilhames
else:
    print 'Impossivel'

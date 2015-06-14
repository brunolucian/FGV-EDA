# coding: utf-8
"""Esse módulo implementa o algoritmo de Ford-Fulkeson"""


class Aresta():
    def __init__(self, origem, destino, capacidade):
        """
        Inicializa uma aresta com sua origem, seu destino e sua capacidade.

        É útil ter um mapeameanto de uma aresta para sua reversa, por
        isso vamos...
        """
        self.origem = origem
        self.destino = destino
        self.capacidade = capacidade
        self.reversa = None


class RedeDeFluxo():
    def __init__(self):
        """Inicializa a rede com uma lista de adjacências vazia e um fluxo vazio."""
        self.adj = {}
        self.fluxo = {}

    def novo_vertice(self, v):
        """Adiciona o vértice v à rede."""
        self.adj[v] = []

    def nova_aresta(self, origem, destino, capacidade):
        """Adiciona uma nova aresta a rede. Também cria a aresta reversa."""
        aresta = Aresta(origem, destino, capacidade)
        self.adj[origem].append(aresta)

        # Criando a aresta reversa
        aresta_reversa = Aresta(destino, origem, 0)
        self.adj[destino].append(aresta_reversa)

        # Marcando aresta e aresta_reversa como reversas uma da outra
        aresta.reversa = aresta_reversa
        aresta_reversa.reversa = aresta

    def novo_fluxo(self, e, f):
        """Adiciona um fluxo f à aresta a."""
        self.fluxo[e] = f

    def encontra_arestas(self, v):
        """Retorna as arestas que partem do vértice v."""
        return self.adj[v]

    def valor_do_fluxo(self, source):
        """Encontra o valor do fluxo, como definido em []."""
        valor = 0
        for aresta in self.encontra_arestas(source):
            valor += self.fluxo[aresta]
        return valor

    def encontra_gargalo(self, caminho):
        """TODO: adicionar explicação aqui."""
        residuos = []
        for aresta in caminho:
            residuos.append(aresta.capacidade - self.fluxo[aresta])
        return min(residuos)

    def expande_caminho(self, caminho):
        """TODO: adicionar explicação aqui."""
        gargalo = self.encontra_gargalo(caminho)
        for aresta in caminho:
            self.fluxo[aresta] += gargalo
            self.fluxo[aresta.reversa] -= gargalo

    def encontra_caminho(self, source, sink, caminho):
        """Retorna um caminho de source a sink passando pelos vértices em caminho."""
        if source == sink:
            return caminho
        for aresta in self.encontra_arestas(source):
            residuo = aresta.capacidade - self.fluxo[aresta]
            if residuo > 0 and aresta not in caminho:
                resp = self.encontra_caminho(aresta.destino,
                                             sink,
                                             caminho + [aresta])
                # TODO: explicar essa parte
                if resp is not None:
                    return resp

    def cria_fluxo_inicial(self):
        """Cria um fluxo inicial com f_e = 0 para toda aresta."""
        for vertice, arestas in self.adj.iteritems():
            for aresta in arestas:
                self.novo_fluxo(aresta, 0)

    def fluxo_maximo(self, source, sink):
        self.cria_fluxo_inicial()
        caminho = self.encontra_caminho(source, sink, [])
        while caminho is not None:
            self.expande_caminho(caminho)
            caminho = self.encontra_caminho(source, sink, [])
        return self.valor_do_fluxo(source)

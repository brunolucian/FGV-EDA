
horarios=[["", "Ana", "Bia", "Caio", "Davi", "Edu", "Felipe", "Gabi", "Hugo", "Isa"], ["Seg 10h", "", "", "", "x", "", "", "", "", ""], ["Seg 14h", "", "", "", "", "", "x", "x", "x", "x"], ["Seg 21h", "x", "", "", "x", "", "", "", "", ""], ["Ter 10h", "x", "x", "", "x", "", "", "", "", ""], ["Ter 16h", "", "", "x", "", "", "", "", "", ""], ["Ter 20h", "", "", "", "", "", "", "x", "", "x"], ["Qua 9h", "", "", "", "", "", "x", "", "", ""], ["Qua 17h", "", "", "x", "", "", "", "", "", ""], ["Qua 19h", "", "", "", "", "", "", "", "x", ""], ["Qui 7h", "", "x", "", "", "", "x", "", "", ""], ["Qui 13h", "", "", "", "", "", "", "x", "", ""], ["Qui 19h", "", "x", "", "", "x", "", "", "x", ""], ["Sex 7h", "", "", "x", "", "x", "", "", "", ""], ["Sex 11h", "x", "", "", "", "x", "", "", "", "x"], ["Sex 21h", "", "", "x", "", "", "x", "", "", "x"]]
regras=[["Min de horas por monitor", 1], ["Max de horas por monitor", 3], ["Horas de monitoria", 10]]
min_por_dia=[["Seg", 1], ["Ter", 1], ["Qua", 2], ["Qui", 1], ["Sex", 1]]
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

    def encontra_caminho(self, v, dreno, caminho, visitados):
        if v == dreno:
            return caminho
    
        visitados.add(v)
    
        for aresta in self.encontra_arestas(v):
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

def cria_rede_com_demandas_nulas(G):
    G_ = RedeDeFluxo()
    G_.novo_vertice('F')
    G_.novo_vertice('D')
    d = 0

    for vertice, arestas in G.adj.iteritems():
        G_.novo_vertice(vertice)
        saldo = sum(e.demanda for e in arestas)
        if saldo > 0:
            G_.nova_aresta(vertice, 'D', saldo, 0)
            d += saldo
        elif saldo < 0:
            G_.nova_aresta('F', vertice, -saldo, 0)

    for arestas in G.adj.values():
        for a in arestas:
             if a.original:
                 G_.nova_aresta(a.origem,
                                a.destino,
                                a.capacidade - a.demanda,
                                0)
    return G_, d

# Lendo a tabela de disponibilidade
intervalos = collections.OrderedDict()
monitores = horarios[0][1:]

for disponibilidade in horarios[1:]:
    intervalos[disponibilidade[0]] = []
    for i, slot in enumerate(disponibilidade[1:]):
        if slot != '':
            intervalos[disponibilidade[0]].append(monitores[i])

min_horas = regras[0][1]
max_horas = regras[1][1]
total_horas = regras[2][1]

minimo_por_dia = {}
for dia in min_por_dia:
    minimo_por_dia[dia[0]] = dia[1]

def cria_rede(intervalos, monitores, min_horas,
              max_horas, total_horas, minimo_por_dia):
    G = RedeDeFluxo()
    G.novo_vertice('Fonte')
    G.novo_vertice('Dreno')
    G.nova_aresta('Dreno', 'Fonte', total_horas, total_horas)

    # Criando um vertice para cada monitor e ligando esse vertice
    # ao dreno
    for monitor in monitores:
        G.novo_vertice(monitor)
        G.nova_aresta(monitor, 'Dreno', max_horas, min_horas)

    # Criando um vertice para cada dia e uma aresta da Fonte
    # ao dia com demanda igual ao minimo de horas de monitoria
    # para aquele dia e capacidade suficientemente grande
    # (vamos usar o total de horas)
    dias = minimo_por_dia.keys()
    for dia in dias:
        G.novo_vertice(dia)
        G.nova_aresta('Fonte', dia, total_horas, minimo_por_dia[dia])

    for intervalo, monitores_disponiveis in intervalos.iteritems():
        # Encontrando o dia do intervalo
        for dia in dias:
            if intervalo.startswith(dia):
                dia_do_intervalo = dia

        # Criando um vertice para cada intervalo e conectando o
        # dia do intervalo a cada um dos intervalos
        G.novo_vertice(intervalo)
        G.nova_aresta(dia_do_intervalo, intervalo, 1, 0)

        # Conectando o intervalo a cada monitor disponivel nele
        for monitor in monitores_disponiveis:
            G.nova_aresta(intervalo, monitor, 1, 0)

    return G

G = cria_rede(intervalos, monitores, min_horas, max_horas, total_horas, minimo_por_dia)
G_, d = cria_rede_com_demandas_nulas(G)
fluxo = G_.fluxo_maximo('F', 'D')
if fluxo == d:
    tabela_de_monitores = []
    for horario in intervalos:
        for w in G_.adj[horario]:
            if G_.fluxo[w] == 1:
                tabela_de_monitores.append([w.origem, w.destino])
    print tabela_de_monitores
else:
    print 'Impossivel'

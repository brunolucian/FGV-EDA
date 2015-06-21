import collections


class Arvore:
    def __init__(self, pai):
        self.filhos = []
        self.label = ""
        self.pai = pai


def parseia_newick(string):
    string = string.replace(',', ')(').replace(';', '')

    em_construcao = collections.deque()
    em_construcao.append(Arvore(None))

    for ch in string:
        if ch == '(':
            pai_atual = em_construcao[-1]
            filho_novo = Arvore(pai_atual)
            pai_atual.filhos.append(filho_novo)
            em_construcao.append(filho_novo)
        elif ch == ')':
            em_construcao.pop()
        else:
            em_construcao[-1].label += ch

    assert len(em_construcao) == 1
    return em_construcao[0]


def arvore_iesimo(i, origem):
    copia_origem = Arvore(None)
    if len(origem.label):
        copia_origem.label = origem.label[i]

    for filho in origem.filhos:
        copia_filho = arvore_iesimo(i, filho)
        copia_filho.pai = copia_origem
        copia_origem.filhos.append(copia_filho)

    return copia_origem


def concatena_arvores(arvores):
    fusao = Arvore(None)
    fusao.label = reduce(lambda string, arv: string + arv.label, arvores, "")

    for i in xrange(len(arvores[0].filhos)):
        fusao_filho = concatena_arvores(map(lambda arvore: arvore.filhos[i],
                                            arvores))
        fusao_filho.pai = fusao
        fusao.filhos.append(fusao_filho)

    return fusao


b = parseia_newick(arvore_newick)

indiv = [' '] * 4
for i in xrange(4):
    indiv[i] = arvore_iesimo(i, b)

a = concatena_arvores(indiv)

print a.filhos[0].filhos[0].filhos[0].label, a.filhos[0].filhos[0].filhos[0].pai
print a.filhos[0].filhos[0].filhos[1].label, a.filhos[0].filhos[0].filhos[1].pai
print a.filhos[0].filhos[0]
print a.filhos[0].filhos[1].label
print a.filhos[1].filhos[0].label
print a.filhos[1].filhos[1].label

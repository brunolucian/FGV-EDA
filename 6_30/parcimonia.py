
arquivo_entrada="livro.in"
import collections

class Arvore:
    def __init__(self, pai):
        self.filhos = []
        self.valor = ""
        self.pai = pai
        self.nome = ""

melhor_nota = {}
melhor_letra = {}

def calcula_melhor_nota(v, l):
    if (v, l) in melhor_nota:
        return melhor_nota[v, l]

    if not v.filhos:
        melhor_nota[v, l] = 1 if l != v.valor else 0
        melhor_letra[v, l] = v.valor
        return melhor_nota[v, l]

    melhor_nota[v, l] = 100000

    for m in ['A', 'G', 'T', 'C', '-']:
        nota_atual = sum(calcula_melhor_nota(w, m) for w in v.filhos)
        if m != l:
            nota_atual += 1

        if nota_atual < melhor_nota[v, l]:
            melhor_nota[v, l] = nota_atual
            melhor_letra[v, l] = m

    return melhor_nota[v, l]

def preenche_tudo(raiz):
    melhor_nota_raiz = 100000
    for l in ['A', 'G', 'T', 'C', '-']:
        nota_atual_raiz = sum(calcula_melhor_nota(w, l) for w in raiz.filhos)

        if nota_atual_raiz < melhor_nota_raiz:
            raiz.valor = l
            melhor_nota_raiz = nota_atual_raiz

    def preenche_dado_pai(v):
        v.valor = melhor_letra[v, v.pai.valor]
        for w in v.filhos:
            preenche_dado_pai(w)

    for w in raiz.filhos:
        preenche_dado_pai(w)

    return raiz, melhor_nota_raiz

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
            em_construcao[-1].nome += ch

    assert len(em_construcao) == 1
    return em_construcao[0]

def fasta_para_dict(linhas):
    nome = ""
    dna = ""
    saida = {}

    for linha_atual in linhas:
        if linha_atual[0] == ">":
            if nome != "":
                saida[nome] = dna
                dna = ""
            nome = linha_atual[1:]
        else:
            dna += linha_atual

    saida[nome] = dna

    return saida

def separa_arvore(indice, origem):
    copia_origem = Arvore(None)
    copia_origem.nome = origem.nome

    if len(origem.valor):
        copia_origem.valor = origem.valor[indice]

    for filho in origem.filhos:
        copia_filho = separa_arvore(indice, filho)
        copia_filho.pai = copia_origem
        copia_origem.filhos.append(copia_filho)

    return copia_origem

def concatena_arvores(arvores):
    fusao = Arvore(None)
    fusao.valor = reduce(lambda string, arv: string + arv.valor,
                         arvores, "")
    fusao.nome = arvores[0].nome

    for i in xrange(len(arvores[0].filhos)):
        fusao_filho = concatena_arvores(
            map(lambda arvore: arvore.filhos[i], arvores))
        fusao_filho.pai = fusao
        fusao.filhos.append(fusao_filho)

    return fusao

def imprime_resposta(arvore):
    if arvore.filhos:
        print '>%s' % arvore.nome
        print arvore.valor

    for w in arvore.filhos:
        imprime_resposta(w)

with open(arquivo_entrada, 'r') as f:
    entrada = map(lambda s: s.strip(), f.readlines())

raiz_grande = parseia_newick(entrada[0])
dnas = fasta_para_dict(entrada[1:])

def preenche_folhas(arvore, dnas):
    if arvore.nome in dnas:
        arvore.valor = dnas[arvore.nome]

    for w in arvore.filhos:
        preenche_folhas(w, dnas)

preenche_folhas(raiz_grande, dnas)

n = len(dnas.values()[0])

arvores_sep = [separa_arvore(i, raiz_grande) for i in range(n)]
pares_preenchidos = [preenche_tudo(a) for a in arvores_sep]

nota_total = sum(nota for (_, nota) in pares_preenchidos)
resposta = concatena_arvores([raiz for (raiz, _) in pares_preenchidos])

print "Nota:", nota_total
imprime_resposta(resposta)

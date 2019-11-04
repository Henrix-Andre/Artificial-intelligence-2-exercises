import random
import math

produtos = [[10,15],[40,90],[20,50],[32,40],[8,12]] #como os "genes" no problema são fixos, a lista aqui é fixa também.
                    # #a lógica segue: [[peso do produto 1, valor do produto 1], [peso do produto 2, val do prod. 2],...]

lPM = 80 #lP = limite de Peso da Mochila, para facilitar testes com uma mochila maior

FEV = 1 #Taxa de mutação, aqui entra como variável global para facilitar testes com taxas maiores.

best = [0,0,0] #a ideia do best é guardar não só a melhor configuração, mas também os valores dela.
           # ex.: best = [[0,0,1,0,1],62,28]; com o primeiro sendo a config, o segundo o valor e o terceiro peso.
           #resumindo: best[0] é a configuração da mochila, best[1] é o valor da config, best[2] é o peso.

def checarAptidao(individuo):
    peso = 0 #peso inicial zero
    #checa cada gene do individuo
    for i in range(0,4):
        #se o individuo pegou o item, contabiliza o peso dele
        if individuo[i] == 1:
            peso += produtos[i][0]
    #se passa do limite ou está vazio, não é apto
    if peso > lPM or peso == 0:
        return False
    #se for apto, só retorna true.
    else:
        return True

def genPop(numInd):
    #vai ter um vetor pra por as listas
    newPop = []
    i = 0
    while i <= numInd :
        newInd = [] #vai gerar um individuo, cada um sendo uma lista de 5 itens.
        for j in range(0,5):
              newInd.append(random.randint(0,1)) #gera os genes do individo, dentro do loop.
                                                 #só 0 (não pegou) e 1 (pegou) já que é em binario.
        if checarAptidao(newInd) == True:
            newPop.append(newInd)  #se o individuo é apto, joga ele na população e continua.
            i += 1
    return newPop #retorna a população.

def checarValor(individuo):
    valor = 0 #peso inicial zero
    #checa cada gene do individuo
    for i in range(0,len(individuo)):
        #se o individuo pegou o item, contabiliza o peso dele
        if individuo[i] == 1:
            valor += produtos[i][1]
    #se passa do limite, não é apto
    return valor

def mutate(individuo):
    mutante = individuo #pega os valores do individuo
    completo = False
    #faz a mutação de acordo com o gene escolhido
    while completo == False:
        gene = random.randint(0, 4)  # escolhe o gene que vai ser mutado
        if mutante[gene] == 1:
            mutante[gene] = 0
        elif mutante[gene] == 0:
            mutante[gene] = 1
        if checarAptidao(mutante) == True:
            #se o novo mutante for apto, retorna ele
            completo = True
        elif checarAptidao(mutante) == False:
            mutante = individuo
    return mutante

def checarMutacao(individuo):
    mutant = individuo
    #como o random gera um valor de 0.0~ até 1, podemos usar para calcular a chance de mutar
    chance = random.random() #checa se vai ter mutação pelo método da roleta
    if chance <= FEV: #se mutar vai chamar a função de mutação
        return mutate(mutant)
    else:
        return mutant #senão só manda o mesmo de volta.

def crossover(populacao, pai, mae):
    #pega o pai e a mae e passa os genes para os filhos
    f1 = pai
    f2 = mae
    completo = False #para garantir que vão ser aptos
    while completo == False:
        pos = random.randint(0, 4) #escolhe ponto de divisão, os genes desse ponto até o final são trocados.
                                   #os antes disso mantem os mesmos do f1/f2.
        if pos == 4: #se for o 4 só faz a troca normalmente
            temp = f1[pos]
            f1[pos] = f2[pos]
            f2[pos] = temp
        else:
            #se for outro troca todos os genes a partir daquele ponto.
            for i in range(pos, 4):
                temp = f1[i]
                f1[i] = f2[i]
                f2[i] = temp
        #se são aptos, checa se vão ter mutações
        if checarAptidao(f1) == True and checarAptidao(f2) == True:
            f1 = checarMutacao(f1)
            f2 = checarMutacao(f2)
            completo = True #processo completo
    #joga os dois novos individuos na população, substituindo os pais
    pai = f1
    mae = f2

#Não foi usado nesse caso mas manti aqui.
def dizimar(populacao,maxpop):
    min = 999 #min é a apdidão do mínimo pra saber quem vai ser retirado.
    max = best[1]
    minPos = 0 #a posicao do menor individuo
    if len(populacao) > maxpop:
        overpopulated = True
        while overpopulated == True: #enquanto está superpopulado
            for i in range(0, len(populacao)):
               #vai checando cada um, vendo qual é o menor existente
               if checarValor(populacao[i]) < min:
                   min = checarValor(populacao[i])
                   minPos = i
            #remove o indivíduo e reseta as variaves de checagem
            populacao.pop(minPos)
            min = 9999
            minpos = 0
            #se não estiver superpopulado, então termina.
            if len(populacao) == maxpop:
                overpopulated = False
        #depois que arruma o tamanho da população, ajusta qual é o melhor.
        bestCheck(populacao)
    else:
        #só checa qual é o melhor
        bestCheck(populacao)

def checarPeso(individuo):
    peso = 0
    #somente um loop pra retornar o peso.
    for i in range(0,5):
        if individuo[i] == 1:
            peso += produtos[i][0]
    return peso

def bestCheck(populacao):
    maxPos = 0
    for i in range(len(populacao)):
        # checa o valor de cada individuo, pegando o melhor
        if best[1] < checarValor(populacao[i]):
            max = checarValor(populacao[i])
            maxPos = i
            best.clear()
            best.append(populacao[maxPos])
            best.append(checarValor(populacao[maxPos]))
            best.append(checarPeso(populacao[maxPos]))
        #ajusta quem é o melhor atual


def chave(objeto):
    #isso apenas precisa para fazer o sort, pois pega qual parte do objeto vai ser baseado o sort
    return objeto[0]

def matchmaking(populacao):
    objetos = []
    melhores = []
    menores = []
    chanceMaiores = 0
    chanceMenores = 0
    posicaoPai = 0
    posicaoMae = 1
    mid = math.ceil(len(populacao)/2)
    for i in range(len(populacao)):
        item = []
        item.append(checarValor(populacao[i]))
        item.append(i)
        objetos.append(item)
    objetos.sort(key=chave, reverse=True) #vai ser decrescente a ordem

    #pega os itens que são maiores
    for i in range(0,mid):
        melhores.append(objetos[i])
        chanceMaiores += objetos[i][0]
    #pega os que são menores
    for i in range(mid, len(populacao)):
        menores.append(objetos[i])
        chanceMenores += objetos[i][0]
    #gera as chances, num float entre 0 e 100
    pai = random.uniform(0,100)
    mae = random.uniform(0,100)
    #com os parentes define quem vai ser
    for i in range(len(melhores)):
        if pai <= (melhores[i][0]*100)/chanceMaiores:
            posicaoPai = melhores[i][1]
            break
    for i in range(len(menores)):
        if mae <= (menores[i][0]*100)/chanceMenores:
            posicaoMae = menores[i][1]
            break
    crossover(populacao,populacao[posicaoPai],populacao[posicaoMae])

def bestGen(populacao, gen):
  maxVal = [0,0]
  for i in range(len(populacao)):
      # checa o valor de cada individuo, pegando o melhor
      if maxVal[1] < checarValor(populacao[i]):
        maxVal.clear()
        maxVal.append(populacao[i])
        maxVal.append(checarValor(populacao[i]))
  print("Melhor da geração", gen, ": ", maxVal)

def geneticRun(epochs, populacao, maxpop):
    maxPos = 0
    epochsUsed = 0
    timesChanged = 0
    max = 0
    for i in range(epochs):
        bestLast = best[1]
        bestCheck(populacao)
        matchmaking(populacao)
        epochsUsed += 1
        print("geração ", epochsUsed, ": ")
        for i in range(0,len(populacao)):
          print(populacao[i], " fitness: ", checarValor(populacao[i]), "; ")
        bestGen(populacao, epochsUsed)
        print("Melhor geral Atual: ", best)
        print("-------------")
        if(best[1] == bestLast):
            timesChanged += 1
        else:
            timesChanged = 0
        if(timesChanged == 4):
          break
    bestCheck(populacao)
    print("Melhor resultado: ", best)
    print("Feito em ", epochsUsed," gerações.")

def main():
    populacao = genPop(10)
    print("Populacao inicial: ")
    for i in range(0,len(populacao)):
      print(populacao[i], " fitness: ", checarValor(populacao[i]), "; ")
    bestGen(populacao,0)
    print("--------------")
    geneticRun(10,populacao,10)

if __name__ == "__main__":
    main()
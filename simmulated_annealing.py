##integrantes do grupo 
#####Matheus Colombo
#####José Vicente Pellicer
#####Lucas Santana Nunes
#####Felipe Emanuel Gimenez do Amaral
#####Luiz Gianvechio


import numpy as np
import random
from random import Random

seed = 5114
#seed aleatoria para escolha de items
myPRNG = Random(seed)

#Numero de itens na pool
n = 150

#valores  e pesos para serem carregados
valores = []
for i in range(0,n):
    valores.append(round(myPRNG.triangular(5,1000,200),1))

pesos = []
for i in range(0,n):
    pesos.append(round(myPRNG.triangular(10,200,60),1))


#Peso Maximo para a carga
pesoMAX = 1500

#cria a solucao inicial
def solucao_inicial():
    pesos_sortidos = np.sort(pesos)

    peso_temp = 0  #rastreador do peso
    i = len(pesos) - 1 #contador regressivo
    num_uns = 0 #numero de 1 necessarios na solucao(1 = item selecionado 0 = item nao selecionado)

    #Seleciona uma solucao inicial nao viavel
    while peso_temp <= pesoMAX:
        peso_temp += pesos_sortidos[i]
        i -= 1
        num_uns += 1

    x = np.zeros(n, dtype=int) #iniciando a array de itens selecionados(150 posicoes todas com 0)
    ind_melhores_valores = np.argsort(valores)[-num_uns:] #indices dos primeiros (=num_ones) com maiores valores
    x[ind_melhores_valores] = 1 #pego alguns dos maiores valores

    return x

    #funcao para avaliar a viabilidade da solucao
def evaluate(x):

    valorTotal = np.dot(x,valores)     #computa os valores da solucao
    pesoTotal = np.dot(x,pesos)    #computa os pesos da solucao

    if pesoTotal > pesoMAX:
        valorTotal = np.nan

    return [valorTotal, pesoTotal]   #retorna uma lisat com os pesos e os valores

    #funcao para fazer 1-flip nas solucoes viznhas de x


def vizinhanca(x, k=1):

    vizinhos = []

    for i in range(0,n):
        vizinhos.append(np.copy(x))
        for j in range(k):
            #fazendo adicao circular
            if (i+j)>0:
                a = i+j-150
            else:
                a = i+j

            if vizinhos[i][a] == 1:
                vizinhos[i][a] = 0
            else:
                vizinhos[i][a] = 1

    return np.array(vizinhos)


t = 100000  #setando temperatura inicial
M = 500    #numero de iteracoes por decrescimo de temperatura
k = 0     #contador principal do main loop

x_init = solucao_inicial()   #pega a solucao inicial
f_init = evaluate(x_init)    #faz a avalicao da solucao inicial
x_curr = np.copy(x_init)     #solucao corrente(atual). comeca sempre com x_init(solucao inicial)
f_curr = evaluate(x_curr)    #f_curr mantem a avaliacao da solucao corrente
print("solucao inicial{}".format(f_curr[0]))

#armazena informacoes para solucoes viaveis
f_valor = []
f_peso = []
f_solucao = []
graph_values = []

#varivel que armazena o total de solucoes checadas
solucoesChecadas = 0


#COMECO DA LOGICA DA BUSCA LOCAL SIMULATED ANNEALING ----------------
done = 0

while done == 0:

    #criterio de parada (temperatura < 1)
    if t<1:
        done = 1

    m = 0
    while m<M:
        solucoesChecadas += 1

        N = vizinhanca(x_curr)            #cria uma lista de todos os vizinhos na vizinhanca da solucao corrente (x_curr)
        s = N[myPRNG.randint(0,len(N)-1)]   #Seleciona randomicamente um vizinho da lista

        #checa a viabilidade da solucao
        try:
            aval_s = evaluate(s)
        except:
            continue

        #Se o vizinho selecionado for uma melhoria da solucao corrente,aceita imediatamente
        #Se nao gera uma distribuicao de probabilidade para aceitar ou nao
        if aval_s[0] >= f_curr[0]:
            x_curr = np.copy(s)
            f_curr = np.copy(aval_s)

            f_solucao.append(x_curr)
            f_valor.append(f_curr[0])
            f_peso.append(f_curr[1])
        else:
            p = np.exp(-(f_curr[0]-aval_s[0])/t)
            test_p = myPRNG.uniform(0,1)

            if test_p<=p:
                x_curr = np.copy(s)
                f_curr = np.copy(aval_s)

                f_solucao.append(x_curr)
                f_valor.append(f_curr[0])
                f_peso.append(f_curr[1])
        m += 1
        print("solucao corrente: {} \n".format(x_curr))
        graph_values.append(f_curr[0])


    #incrementando contador e diminuindo a temperatura
    k += 1
    t = 0.8*t  #funcao cauchy cooling

print ("\nNumero final de solucoes checadas: ", solucoesChecadas)
print ("Melhor valor encontrado: ", np.nanmax(f_valor))
print ("Peso da solucao: ", f_peso[np.nanargmax(f_valor)])
print ("Total de itens selecionados: ", np.sum(x_curr))
print ("Melhor solucao: ", x_curr)

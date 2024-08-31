import time
import random
import matplotlib.pyplot as plt

# Algoritmo iterativo
def mochila_iterativa(c, p, l, n):
    m_lucro = [[0 for _ in range(c + 1)] for _ in range(n + 1)] # Inicializar a matriz de lucros
    for i in range(1, n + 1):
        for j in range(1, c + 1):
            if p[i - 1] <= j: # Se o peso do item for menor ou igual à capacidade da mochila
                m_lucro[i][j] = max(m_lucro[i - 1][j], l[i - 1] + m_lucro[i - 1][j - p[i - 1]])
            else:
                m_lucro[i][j] = m_lucro[i - 1][j]
    return m_lucro[n][c]

# Algoritmo recursivo com memoização
def mochila_recusiva(c, p, l, n, m_lucro):
    # Verifica se a capacidade da mochila ou o número de itens é igual a zero
    if n == 0 or c == 0:
        return 0
    # Verifica se o valor já foi calculado e armazenado na matriz de lucros
    if m_lucro[n][c] != -1:
        return m_lucro[n][c]
    # Verifica se o peso do item atual é maior que a capacidade da mochila
    if p[n-1] > c:
        # Chama a função recursivamente para o próximo item
        m_lucro[n][c] = mochila_recusiva(c, p, l, n-1, m_lucro)
    else:
        # Calcula o lucro máximo considerando a inclusão e a exclusão do item atual
        m_lucro[n][c] = max(mochila_recusiva(c, p, l, n-1, m_lucro), l[n-1] + mochila_recusiva(c-p[n-1], p, l, n-1, m_lucro))
    # Retorna o lucro máximo para a capacidade da mochila e o número de itens atual
    return m_lucro[n][c]

# Algoritmo recursivo com memoização que cria a matriz de lucros
def mochila_m(c, p, l, n):
    m_lucro = [[-1 for _ in range(c + 1)] for _ in range(n + 1)]
    return mochila_recusiva(c, p, l, n, m_lucro)

# Função para gerar entradas aleatórias
def gerar_entradas(n, max_peso, max_lucro):
    pesos = [random.randint(1, max_peso) for _ in range(n)]
    lucros = [random.randint(1, max_lucro) for _ in range(n)]
    return pesos, lucros

# Função para medir o tempo de execução de uma função
def medir_tempo_execucao(func, *args):
    inicio = time.perf_counter()
    func(*args) # Executar a função passada como argumento "mochila_m" ou "mochila_iterativa"
    fim = time.perf_counter()
    return fim - inicio

# Função para comparar os algoritmos recursivo e iterativo
def comparar_algoritmos(tamanhos, m, max_peso, max_lucro, capacidade):
    tempos_memo = [] # Lista para armazenar os tempos de execução do algoritmo recursivo
    tempos_iter = [] # Lista para armazenar os tempos de execução do algoritmo iterativo
    tamanho = []
    
    for n in range(5, tamanhos + 1): # Para cada tamanho de entrada
        tempo_memo = 0
        tempo_iter = 0
        tamanho.append(n)
        for _ in range(m):
            pesos, lucros = gerar_entradas(n, max_peso, max_lucro) # Gerar entradas aleatórias
            tempo_iter += medir_tempo_execucao(mochila_iterativa, capacidade, pesos, lucros, n) # Medir o tempo de execução do algoritmo iterativo
            tempo_memo += medir_tempo_execucao(mochila_m, capacidade, pesos, lucros, n) # Medir o tempo de execução do algoritmo recursivo
        
        tempos_iter.append(tempo_iter / m) # Calcular o tempo médio de execução do algoritmo iterativo
        tempos_memo.append(tempo_memo / m) # Calcular o tempo médio de execução do algoritmo recursivo
    
    return tempos_memo, tempos_iter, tamanho, pesos, lucros

# Função para plotar os resultados obtidos
def plotar_resultados(tamanhos, tempos_memo, tempos_iter):
    plt.plot(tamanhos, tempos_iter, label='Iterativo')
    plt.plot(tamanhos, tempos_memo, label='Recursivo')
    plt.xlabel('Tamanho da Entrada (n)')
    plt.ylabel('Tempo de Execução Médio (s)')
    plt.legend()
    plt.title('Comparação de Algoritmos de Programação Dinâmica')
    plt.show()

# Parâmetros para a comparação
max_tamanhos = 50 # Tamanhos das entradas ou quantidade de itens
m = 100 # Número de repetições para medir o tempo médio
max_peso = 50 # Peso máximo dos itens
max_lucro = 1000 # Lucro máximo dos itens    
capacidade = 50 # Capacidade da mochila

# Comparar os algoritmos e obter os resultados
tempos_memo, tempos_iter, tamanho, pessos, lucros = comparar_algoritmos(max_tamanhos, m, max_peso, max_lucro, capacidade)

# Plotar os resultados obtidos
plotar_resultados(tamanho, tempos_memo, tempos_iter)
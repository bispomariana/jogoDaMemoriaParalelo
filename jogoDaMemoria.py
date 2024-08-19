"""
Explicação do jogo: Consiste em um jogo da memória paralelo, onde há um vetor com quatro duplas de cartas e cada thread, ao "descobrir" uma carta, a coloca em seu buffer.
Quando ela conseguir combinar duas iguais em seu buffer, ela pode marcar aquelas cartas no vetor original como dela (apenas a primeira thread que conseguir).
Ganha quem marcar mais cartas!
"""

import random
import time
from concurrent.futures import ThreadPoolExecutor
    

# Criando o vetor com 8 cartas
# Cada carta é representada como uma tupla (valor, proprietário). O valor é uma letra (A, B, C, D), e o proprietário será o thread_id de quem marcou a carta.
cartas = [("A", None), ("A", None), ("B", None), ("B", None), ("C", None), ("C", None), ("D", None), ("D", None)]
random.shuffle(cartas) # Embaralha
        
# Tentativas de cada thread
qtde_tentativas = 30

# Função que as threads irão executar
def procuraCartas(thread_id):

    # Cria um vetor para armazenar as cartas
    buffer = []
    # Define aleatoriamente as posições que vai tentar acessar
    posicoes = [random.randint(0,len(cartas)-1) for _ in range(qtde_tentativas)]
    
    # Acessa cada posição
    for pos in posicoes:
        
        print(f"Thread {thread_id} tentando adquirir uma carta...")
        try:
            # Conseguiu o acesso ao vetor das cartas
            print(f"Thread {thread_id} conseguiu adquirir o vetor de cartas.")
            time.sleep(random.uniform(0.01,0.1)) # Simula carga de trabalho
                
            buffer.append((cartas[pos], pos)) # Adiciona uma carta ao seu buffer    
            print(f"Thread {thread_id} pegou uma carta: {cartas[pos][0]} na posição {pos}")
                            
            # Se certificando que a thread não guarde mais que 3 cartas em seu buffer
            # FIFO com tamanho máximo = 3
            if len(buffer) > 3:
                del buffer[0]
                
            # Verifica se conseguiu combinar 2 cartas iguais.
            # Caso sim, marca-as no vetor principal, caso não pertençam a nenhuma outra thread.
            if len(buffer) >= 2:
                for i in range(len(buffer)):
                    for j in range(i + 1, len(buffer)):
                        if buffer[i][0][0] == buffer[j][0][0] and buffer[i][1] != buffer[j][1]:
                            if cartas[buffer[i][1]][1] == None and cartas[buffer[j][1]][1] == None:
                                cartas[buffer[i][1]] = (cartas[buffer[i][1]][0], thread_id)
                                cartas[buffer[j][1]] = (cartas[buffer[j][1]][0], thread_id)
                                print(f"Thread {thread_id} combinou a carta {cartas[buffer[i][1]][0]} nas posições {buffer[i][1]} e {buffer[j][1]}")
                    
        finally:
            print(f"Thread {thread_id} acaba de liberar o Lock.")

def main():
    # Threads
    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.submit(procuraCartas, 1)
        executor.submit(procuraCartas, 2)
        executor.submit(procuraCartas, 3)
    
    # Inicializa variáveis para contar quantas cartas cada vetor conseguiu marcar
    cartas1 = 0
    cartas2 = 0
    cartas3 = 0
    
    for carta in cartas:
        if carta[1] == 1:
            cartas1+=1
        elif carta[1] == 2:
            cartas2+=1
        elif carta[1] == 3:
            cartas3+=1
    
    print()
        
    # Verifica quem venceu ou se houve empate
    if cartas1 > cartas2 and cartas1 > cartas3:
        print("Thread 1 ganhou")
    elif cartas2 > cartas1 and cartas2 > cartas3:
        print("Thread 2 ganhou")
    elif cartas3 > cartas2 and cartas3 > cartas1:
        print("Thread 3 ganhou")
    else:
        print("Houve empate")
        
    print()
    # Mostra o vetor de cartas após a execução das threads
    print("Resultado Final:")
    print(cartas)

if __name__ == "__main__":
    main()
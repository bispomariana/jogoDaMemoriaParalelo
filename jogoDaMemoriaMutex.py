# Explicacao do jogo: Consiste em um jogo da memória paralelo, onde há um vetor com cartas (duas iguais de cada) e cada thread, ao "descobrir" uma carta, a coloca em seu buffer.
# Quando ela conseguir combinar duas iguais em seu buffer, ela pode marcar aquelas cartas no vetor original como dela (apenas a primeira thread que conseguir).
# Ganha quem marcar mais cartas!

import random
import time
from concurrent.futures import ThreadPoolExecutor

# Criando o vetor com 8 cartas
cartas = [("A", None), ("A", None), ("B", None), ("B", None), ("C", None), ("C", None), ("D", None), ("D", None)]
random.shuffle(cartas)  # embaralha

# Tentativas de cada thread
qtde_tentativas = 30

# Mutex
interessados = [False, False, False]
vez = -1

def entraRegiaoCritica(thread_id):
    pont = 0
    global vez
    thread_id -= 1
    interessados[thread_id] = True
    if thread_id == 0 or thread_id == 1:
        vez = thread_id + 1
        pont = thread_id + 1
    else:
        vez = 0
        pont = 0
    
    while interessados[pont] and vez == pont:
        pass
    
def saiRegiaoCritica(thread_id):
    interessados[thread_id - 1] = False

# Função que as threads vão executar
def procuraCartas(thread_id):
    # cria um vetor para armazenar as cartas
    buffer = []
    # define as posições que vai tentar acessar
    posicoes = [random.randint(0, len(cartas) - 1) for _ in range(qtde_tentativas)]

    # acessa
    for pos in posicoes:
        print(f"Thread {thread_id} tentando adquirir alguma carta...")
        entraRegiaoCritica(thread_id)
        try:
                print(f"Thread {thread_id} conseguiu adquirir o vetor de cartas.")
                time.sleep(random.uniform(0.01, 0.1))

                # Adiciona a carta ao buffer
                buffer.append((cartas[pos], pos))
                print(f"Thread {thread_id} pegou uma carta: {cartas[pos][0]} na posição {pos}")

                # não deixa guardar mais que 3
                if len(buffer) > 3:
                    del buffer[0]

                # verifica se conseguiu 2 cartas iguais e altera lá no vetor principal
                if len(buffer) >= 2:
                    for i in range(len(buffer)):
                        for j in range(i + 1, len(buffer)):
                            if buffer[i][0][0] == buffer[j][0][0] and buffer[i][1] != buffer[j][1]:
                                if cartas[buffer[i][1]][1] is None and cartas[buffer[j][1]][1] is None:
                                    cartas[buffer[i][1]] = (cartas[buffer[i][1]][0], thread_id)
                                    cartas[buffer[j][1]] = (cartas[buffer[j][1]][0], thread_id)
                                    print(f"Thread {thread_id} combinou a carta {cartas[buffer[i][1]][0]} nas posições {buffer[i][1]} e {buffer[j][1]}")
                                    
        finally:
                saiRegiaoCritica(thread_id)
                print(f"Thread {thread_id} acaba de liberar o vetor.")

# Threads
def main():
    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.submit(procuraCartas, 1)
        executor.submit(procuraCartas, 2)
        executor.submit(procuraCartas, 3)
        
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
        
    if cartas1 > cartas2 and cartas1 > cartas3:
        print("Thread 1 ganhou")
    elif cartas2 > cartas1 and cartas2 > cartas3:
        print("Thread 2 ganhou")
    elif cartas3 > cartas2 and cartas3 > cartas1:
        print("Thread 3 ganhou")
    else:
        print("Houve empate")
        
    print()
    print("Resultado Final:")
    print(cartas)
        
if __name__ == "__main__":
    main()

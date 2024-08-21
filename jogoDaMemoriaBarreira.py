import threading
import random
import time
from concurrent.futures import ThreadPoolExecutor

class Barreira:
    def __init__(self, n):
        self.threads = n
        self.contador = 0 # Conta quantas threads já alcançaram a barreira
        self.lock = threading.Lock()
        self.trava = threading.Condition(self.lock) # Bloqueia e notifica as threads

    def deveEsperar(self):
        with self.trava:
            self.contador += 1
            if self.threads == self.contador: # Verifica se todas as threads já chegaram
                self.trava.notify_all() # Desbloqueia todas as threads
                self.contador = 0 # Reinicia
            else:
                self.trava.wait() # Faz com que a thread espere até todas chegarem


# Definindo o vetor com 8 cartas
# Cada carta é representada como uma tupla (valor, proprietário). O valor é uma letra (A, B, C, D), e o proprietário será o thread_id de quem marcou a carta.
cartas = [('B', None), ('C', None), ('D', None), ('D', None), ('A', None), ('B', None), ('A', None), ('C', None)]

# Tentativas de cada thread
qtde_tentativas = 30

#Barreira
barreira = Barreira(3)

# Função que as threads vão executar
def procuraCartas(thread_id, vetor_posicoes):
    
    # Cria um vetor para armazenar as cartas
    buffer = []
    # Define as posições que irá acessar
    posicoes = vetor_posicoes
    qtde = 0 # Quantidade de posições que já foram acessadas

    # Acessa cada posição
    for pos in posicoes:
        qtde += 1
        print(f"Thread {thread_id} tentando adquirir uma carta...")
        try:
            # Conseguiu o acesso ao vetor das cartas
            print(f"Thread {thread_id} conseguiu adquirir o vetor de cartas.")
            time.sleep(random.uniform(0.01, 0.1)) # Simula carga de trabalho

            buffer.append((cartas[pos], pos)) # Adiciona uma carta ao seu buffer  
            print(f"Thread {thread_id} pegou uma carta: {cartas[pos][0]} na posição {pos}")

            # Se certificando que a thread não guarde mais que 3 cartas em seu buffer
            # FIFO com tamanho máximo = 3
            if len(buffer) > 3:
                del buffer[0]

            # Verifica se conseguiu combinar 2 cartas iguais
            # Caso sim, marca-as no vetor principal, caso não pertençam a nenhuma outra thread
            if len(buffer) >= 2:
                for i in range(len(buffer)):
                    for j in range(i + 1, len(buffer)):
                        if buffer[i][0][0] == buffer[j][0][0] and buffer[i][1] != buffer[j][1]:
                            if cartas[buffer[i][1]][1] == None and cartas[buffer[j][1]][1] == None:
                                cartas[buffer[i][1]] = (cartas[buffer[i][1]][0], thread_id)
                                cartas[buffer[j][1]] = (cartas[buffer[j][1]][0], thread_id)
                                print(f"Thread {thread_id} combinou a carta {cartas[buffer[i][1]][0]} nas posições {buffer[i][1]} e {buffer[j][1]}")
        finally:
            print(f"Thread {thread_id} acaba de liberar o vetor.")
            
        # Se a thread completou 1/3 das tentativas, chega à barreira
        # A cada 10 tentativas, ela chega à barreira
        if qtde % (qtde_tentativas // 3) == 0:
            print(f"Thread {thread_id} chegou à barreira")
            barreira.deveEsperar()

def main():
    # Threads
    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.submit(procuraCartas, 1, [3, 6, 2, 0, 1, 7, 4, 6, 3, 6, 1, 5, 0, 6, 3, 7, 4, 7, 3, 5, 0, 1, 7, 3, 0, 1, 3, 1, 4, 7])
        executor.submit(procuraCartas, 2, [7, 2, 5, 5, 5, 6, 6, 4, 5, 2, 1, 0, 5, 4, 6, 7, 2, 3, 5, 5, 0, 1, 7, 3, 4, 6, 4, 1, 3, 7])
        executor.submit(procuraCartas, 3, [3, 7, 2, 2, 7, 1, 6, 1, 2, 4, 6, 5, 0, 0, 0, 4, 2, 3, 0, 6, 4, 5, 3, 0, 4, 6, 3, 1, 5, 7])
        
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

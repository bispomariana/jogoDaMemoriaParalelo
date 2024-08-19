import random
import time
from concurrent.futures import ThreadPoolExecutor

class Semaforo:
    def __init__(self, valor_inicial=1):
        self.contador = valor_inicial
        self.condicao = False #Sinaliza a espera
        
    # Sinaliza que a thread está tentando acessa o recurso
    def entrada(self):
        while self.contador <= 0: # Espera enquanto o recurso não está disponível
            self.condicao = True
        self.contador -= 1
        self.condicao = False

    # Libera o acesso ao recurso
    def saida(self):
        self.contador += 1
        if self.condicao:
            self.condicao = False

# Definindo o vetor com 8 cartas
# Cada carta é representada como uma tupla (valor, proprietário). O valor é uma letra (A, B, C, D), e o proprietário será o thread_id de quem marcou a carta.
cartas = [('B', None), ('C', None), ('D', None), ('D', None), ('A', None), ('B', None), ('A', None), ('C', None)]

# Tentativas de cada thread
qtde_tentativas = 30

#Semáforo
semaforo = Semaforo(1)

# Função que as threads irão executar
def procuraCartas(thread_id, vetor_posicoes):
    
   # Cria um vetor para armazenar as cartas
    buffer = []
    # Define as posições que irá acessar
    posicoes = vetor_posicoes

    # Acessa cada posição
    for pos in posicoes:
        print(f"Thread {thread_id} tentando adquirir uma carta...")
        semaforo.entrada() # Tenta acessar o vetor
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
            semaforo.saida()
            print(f"Thread {thread_id} acaba de liberar o vetor.")

def main():
    # Threads
    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.submit(procuraCartas, 1, [3, 6, 2, 0, 0, 7, 1, 2, 3, 6, 1, 6, 3, 6, 3, 7, 4, 7, 3, 5, 1, 1, 4, 3, 0, 1, 3, 1, 4, 1])
        executor.submit(procuraCartas, 2, [7, 2, 5, 5, 5, 6, 6, 4, 5, 2, 1, 6, 5, 4, 6, 7, 2, 5, 5, 5, 3, 1, 2, 3, 2, 6, 4, 1, 3, 7])
        executor.submit(procuraCartas, 3, [4, 7, 5, 2, 2, 3, 6, 1, 2, 4, 6, 5, 0, 0, 0, 4, 2, 3, 0, 6, 4, 5, 3, 0, 4, 4, 3, 7, 5, 7])
        
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

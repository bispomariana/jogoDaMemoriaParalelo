# Jogo da Memória Paralelo

## Descrição do Projeto

O "Jogo da Memória Paralelo" é uma implementação do clássico jogo da memória utilizando programação paralela com threads. Este projeto demonstra a interação entre múltiplas threads tentando descobrir e combinar pares de cartas em um vetor compartilhado. O objetivo principal é capturar os momentos em que acontecem condições de corrida e implementar 4 possíveis soluções: mutex, semáforo, barreira e troca de mensagens.

## Índice

   [Descrição](#descrição-do-projeto) |    [Índice](#índice) | [Funcionalidades](#funcionalidades) | [Como executar](#como-executar) | [Pré-Requisitos](#pré-requisitos) | [Rodando o programa](#rodando-o-programa) | [Instruções de uso](#instruções-de-uso) | [Tecnologias](#tecnologias) | [Contribuições](#contribuições) | [Autor](#autor) | [Licença](#licença)

## Status do projeto: Concluído

## Funcionalidades

O projeto possui as seguintes funcionalidades:

- Sincronização de threads por meio de lock (mutex).
- Sincronização de threads por meio de semáforo.
- Sincronização de threads por meio de barreira.
- Sincronização de threads por meio de troca de mensagens.
 
## Como executar

### Pré-Requisitos
Certifique-se de ter o [Python 3.x](https://www.python.org/downloads/) instalado em sua máquina.

IDE de sua escolha. (Opcional)

### Rodando o programa

1. Clone ou faça o download deste repositório.

#### No Terminal: 

2. Navegue até o diretório do projeto:
```
> cd /caminho/para/o/diretório/do/projeto
```
3. Execute o arquivo Python:
```
> python nome_do_arquivo.py
```

#### Por uma IDE:

2. Abra o projeto na sua IDE (ex: PyCharm, VSCode).
3. Execute os arquivos na IDE.

### Instruções de uso
Após executar o programa, o jogo da memória será inicializado automaticamente.

* Funcionamento:

Cada thread revela cartas em posições aleatórias do vetor de cartas. Quando uma thread consegue formar um par de cartas iguais, se nenhuma outra já houver formado esse par, ela marca essas cartas como suas no vetor compartilhado. Ganha a thread que ao final das tentativas tiver marcado mais cartas.

* Obs.: O arquivo `jogoDaMemoria.py` mostra a lógica do jogo, mas para ser possível comparar detalhes como velocidade e eficácia, os valores de `posicoes` e `cartas` já foram definidos igualmente nos outros arquivos.

## Tecnologias
- [Python](https://www.python.org/)
- [VSCode](https://code.visualstudio.com/)

## Contribuições
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests. Todo feedback ou sugestão será considerado.

## Autor
Feito por Mariana Bispo.

![Static Badge](https://img.shields.io/badge/Mariana%20Bispo%20-%20%230e76a8?logo=linkedin&link=www.linkedin.com%2Fin%2Fmariana-bispo-840653263)

![Static Badge](https://img.shields.io/badge/msb19112004%40gmail.com%20-%20%23db4a39?logo=gmail&logoColor=white&link=mailto%3Amsb19112004%40gmail.com)



## Licença

[MIT](https://choosealicense.com/licenses/mit/)
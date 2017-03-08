# blackjack
IIA - Blackjack

Projeto da disciplina Introdução à Inteligência Artificial (IIA) - DETI-UA 2016

Cristiano Vagos (cristianovagos@ua.pt) - 65169<br>
João Pedro Fonseca (jpedrofonseca@ua.pt) - 73779

------------------------------------------------------------------------------------------------

Agente que joga sozinho Blackjack, com o código fornecido pelos professores.
Optámos por escolher a estratégia de AI Reinforcement Learning, que faz com que o agente aprenda sozinho a tomar decisões conforme os jogos que vai fazendo e os resultados obtidos dos mesmos.<br>
(Fonte: livro "Reinforcement Learning: An Introduction")<br>
(link: https://webdocs.cs.ualberta.ca/~sutton/book/bookdraft2016sep.pdf)

Algumas ideias aqui implementadas são baseadas em código já existente, onde são feitos dois métodos de Reinforcement Learning (Monte Carlo ES e Q-Learning):<br>
(código: https://inst.eecs.berkeley.edu/~cs188/sp08/projects/blackjack/blackjack.py)

A nossa estratégia passa por jogar de forma completamente aleatória até um número limite de jogadas para cada estado possível. Então, os dados são guardados em 2 dicionários que guardam todos os estados possíveis e a probabilidade de acerto, que é aumentada/diminuida conforme a recompensa de cada jogo (1 em caso de vitória, 0 para empate, -1 para derrota).
Todas as acções são escolhidas pelo agente, de forma completamente autónoma tendo em base os jogos que já efetuou até ao momento.

Depois do número limite de jogadas para cada tipo de jogada (Hit, Stand ou Double-Down) o agente joga a melhor opção determinada pelo histórico de jogos que fez até ao momento.
A melhor acção provém do dicionário respetivo (primeira / próximas jogadas), e é escolhida a acção que tem a maior média de recompensa (quanto mais próximo de 1, melhor, e quanto mais próximo de -1 pior).
Por isso o rácio de vitórias irá aumentar ao longo do tempo em que a tabela é preenchida.

Guardamos os dados (Tabelas Q + Contagens de Ocorrências) num ficheiro que é habitualmente lido e gravado com os dados que vai obtendo no decorrer dos jogos. Conforme o estado do jogo atual (mão do dealer, mão do jogador, se o jogador tem "hard" ou "soft hand"), o agente escolhe então uma opção de entre as disponíveis (Hit / Stand / Double-Down / Surrender).

O sistema de apostas usado no nosso agente é o "Up and Pull Betting System".<br>
(Retirado de: http://www.countingedge.com/blackjack-money-management/)<br>
Após os testes confirma-se que é uma boa estratégia de apostas para um bom ganho e menor risco.

------------------------------------------------------------------------------------------------

Packages não-nativos necessários à execução: numpy (studentPlayer.py), termcolor (print_studentPlayer.py)

------------------------------------------------------------------------------------------------

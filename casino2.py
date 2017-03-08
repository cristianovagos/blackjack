from game import Game
from player import Player
from randomplayer import RandomPlayer
from studentPlayer import StudentPlayer

if __name__ == '__main__':
    startmoney = money = 100

    #players = [StudentPlayer("Eu",startmoney), RandomPlayer("José", startmoney), RandomPlayer("Pedro", startmoney), RandomPlayer("António", startmoney)]
    players = [StudentPlayer("Eu", startmoney)]
    games = 0
    wins = 0
    profit = 0

    for i in range(10000000):
        aux = players[0].pocket
        g = Game(players, min_bet=1, max_bet=5)
        #g = Game(players, debug=True)
        g.run()
        games += 1
        money = players[0].pocket
        if money > aux:
            profit += (money - aux)
            wins += 1

    print("OVERALL: ", players)
    print("Games: ", games)
    print("Wins: ", wins)
    print("Win rate: ", wins/games*100)
    print("Profit from victories: ", profit)
    print("Overall Profit: ", money - startmoney)
    print("Profit?: ", money > startmoney)
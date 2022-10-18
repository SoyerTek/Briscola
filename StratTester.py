from threading import Thread

from Board import Board
from Player import Player
from Strategy import DefaultStrategy, SimpleStrategy, Strategy


def simpleTest(p1Strategy : Strategy, p2Strategy : Strategy, verbose=False):
    board = Board()
    Player("Mario", board, p1Strategy)
    Player("Luigi", board, p2Strategy)

    for i in range(40):
        board.nextPlay()
    
    if verbose == True:
        print("ha vinto " + str(board.eval()))

def steppedTest(runs, step, p1Strategy : Strategy, p2Strategy : Strategy, actual=True, verbose=False):
    threads = []
    for i in range(int(runs/step)):
        t = StratTester()
        t.setup(step, p1Strategy, p2Strategy, verbose)
        threads.append(t)

    if(actual==True):
        for t in threads:
            t.start()
        for t in threads:
            t.join()
    else:
        for t in threads:
            t.run()



class StratTester(Thread):

    def setup(self, runs, p1Strategy : Strategy, p2Strategy : Strategy, verbose=False):
        self._runs = runs
        self._p1Strat = p1Strategy
        self._p2Strat = p2Strategy
        self._verbose = verbose


    def run(self) -> None:
        for a in range(self._runs):
            simpleTest(self._p1Strat, self._p2Strat, self._verbose)
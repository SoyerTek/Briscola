from threading import Thread
from unittest import result

from Board import Board
from Player import Player
from Strategy import DefaultStrategy, SimpleStrategy, Strategy


def simpleTest(p1Strategy : Strategy, p2Strategy : Strategy, verbose=False):
    """
    Execute 1 full game betwen p1Strategy and p2Strategy, verbose==True prints the result
    """
    board = Board()
    Player("Mario", board, p1Strategy)
    Player("Luigi", board, p2Strategy)

    for i in range(40):
        board.nextPlay()
    
    if verbose == True:
        print("ha vinto " + str(board.eval()))
    
    return board.eval()

def steppedTest(runs, step, p1Strategy : Strategy, p2Strategy : Strategy, threaded=True, verbose=False):
    """
    Executes runs/step games betwen p1Strategy and p2Strategy,
    threaded==True executes them at the same time
    verbose==True prints the result
    """
    results = []
    threads = []
    for i in range(int(runs/step)):
        t = StratTester()
        t.setup(step, p1Strategy, p2Strategy, verbose)
        threads.append(t)

    if(threaded==True):
        for t in threads:
            t.start()
        for t in threads:
            t.join()
            results.append(t.wonByP1)
    else:
        for t in threads:
            t.run()
            results.append(t.wonByP1)
    
    return results


class StratTester(Thread):

    @property
    def wonByP1(self):
        return self._runs-self._wonByP2
    
    @property
    def wonByP2(self):
        return self._wonByP2

    def setup(self, runs, p1Strategy : Strategy, p2Strategy : Strategy, verbose=False):
        self._runs = runs
        self._p1Strat = p1Strategy
        self._p2Strat = p2Strategy
        self._verbose = verbose
        self._wonByP2 = 0


    def run(self) -> None:
        for a in range(self._runs):
            self._wonByP2 += simpleTest(self._p1Strat, self._p2Strat, self._verbose)
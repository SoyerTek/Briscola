from threading import Thread
from unittest import result

from Board import Board
from Player import Player
from Strategy import Strategy


def simpleTest(p1Strategy : Strategy, p2Strategy : Strategy, verbose=0):
    """
    Execute 1 full game betwen p1Strategy and p2Strategy, verbose==True prints the result
    """
    board = Board(True if verbose==2 else False)
    Player("Player0", board, p1Strategy)
    Player("Player1", board, p2Strategy)

    for i in range(40):
        board.nextPlay()
    
    if verbose >= 1:
        print(board._players[board.eval()]._name+" wins!")
    
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
        self._verbose = 1 if verbose else 0
        self._wonByP2 = 0


    def run(self) -> None:
        for a in range(self._runs):
            self._wonByP2 += simpleTest(self._p1Strat, self._p2Strat, self._verbose)
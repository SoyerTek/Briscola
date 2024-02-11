from threading import Thread

from Board import Board
from Player import Player
from Strategy import Strategy


def simpleTest(p1Strategy: Strategy, p2Strategy: Strategy, verbose=0):
    """
    Execute 1 full game betwen p1Strategy and p2Strategy, verbose==1 prints the result, 2 step by step
    """
    board = Board(verbose == 2)
    Player("Player0", board, p1Strategy)
    Player("Player1", board, p2Strategy)

    for i in range(40):
        board.nextPlay()

    if verbose >= 1:
        print(board._players[board.eval()]._name + " wins!")

    return board.eval()


def steppedTest(runs, step, p1Strategy: Strategy, p2Strategy: Strategy, threaded=True, verbose=False):
    """
    Executes runs/step games betwen p1Strategy and p2Strategy,
    threaded==True executes them at the same time
    verbose==True prints the result
    """
    results = []
    threads = []
    for i in range(int(runs / step)):
        tester = StratTester()
        tester.setup(step, p1Strategy, p2Strategy, verbose)
        threads.append(tester)

    if threaded == True:
        for tester in threads:
            tester.start()
        for tester in threads:
            tester.join()
            results.append(tester.wonByP1)
    else:
        for tester in threads:
            tester.run()
            results.append(tester.wonByP1)

    return results


class StratTester(Thread):

    @property
    def wonByP1(self):
        return self._runs - self._wonByP2

    @property
    def wonByP2(self):
        return self._wonByP2

    def setup(self, runs, p1Strategy: Strategy, p2Strategy: Strategy, verbose=False):
        self._runs = runs
        self._p1Strat = p1Strategy
        self._p2Strat = p2Strategy
        self._verbose = int(verbose)
        self._wonByP2 = 0

    def run(self) -> None:
        for a in range(self._runs):
            self._wonByP2 += simpleTest(self._p1Strat, self._p2Strat, self._verbose)

from Board import Board
from Player import Player
from StratTester import StratTester, simpleTest, steppedTest
from Strategy import DefaultStrategy, SimpleStrategy
import time


#simpleTest(DefaultStrategy(), SimpleStrategy())
for i in range(5) :
    start_time = time.time()
    steppedTest(200, 50, DefaultStrategy(), SimpleStrategy(), True)

    print("--- %s seconds ---" % str((time.time() - start_time)).replace(".", ","))



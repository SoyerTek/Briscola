from Board import Board
from Player import Player
from StratTester import StratTester, simpleTest, steppedTest
from Strategy import DefaultStrategy, HumanStrategy, MiniMaxStrategy, SimpleStrategyV1, SimpleStrategyV2, SimpleStrategyV5, Strategy
import time

def stupiTest(strats, number):
    for s1 in strats:
        for s2 in strats:
            print(str(s1)+" vs " + str(s2) +" "+ str(number)+" runs in " + str(int(number/5/5)) +" games ")
            avgs = []
            total = 0
            count = 0
            for i in range(5) :
                start_time = time.time()
                results = steppedTest(int(number/5), int(number/5/5), s1, s2, 0)
                avgs.append(sum(results) / len(results))
                total+=sum(results)
                count+=len(results)

                print(results)
                print("--- %s seconds ---" % str((time.time() - start_time)).replace(".", ","))

            print(avgs)
            print(total/count)
            print(total/(count*(number/5/5)))

    #2,46 123,49 200-100-False
    #2.47 123,81 200-20-False
    #2,93 146,83 200-20-True
    #2.87 143.64 200-100-True
    #2.48 124,39 200-Sequential


simpleTest(MiniMaxStrategy(10), HumanStrategy(), 2)
#stupiTest([SimpleStrategyV2(), MiniMaxStrategy(5)], 250)
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

        
simpleTest(SimpleStrategyV5(), SimpleStrategyV5(), 2)
start_time = time.time()
#print(steppedTest(20, 5, SimpleStrategyV5(), SimpleStrategyV2(), True, True))
print("--- %s seconds ---" % str((time.time() - start_time)).replace(".", ","))
#stupiTest([SimpleStrategyV2(), MiniMaxStrategy()], 250)
import sys
import csv
import time
from all_on_demand_cost import get_all_od_cost

#total_purchases.csv
#reserve_prt1y_code.csv

def main():
    start_time = time.time()
    total_purchases_path = sys.argv[1]
    demand_path = sys.argv[2]
    prices_path = sys.argv[3]

    max_t = 26302
    opt_vs_all_od = [[i, 0, 0] for i in range(max_t + 1)]
    od_vs_re = [[i, 0, 0] for i in range(max_t + 1)]

    prices = get_prices(prices_path)
    
    print('Starting to iterate over total purchases: ' + str((time.time() - start_time) / 60))  
    with open(total_purchases_path, mode='r') as file:
        while True:
            line = file.readline()
            if not line:
                break
            #line: timeId, instanceType, market, count
            timeId, instanceType, market, count = line.split(',')
            if timeId == 'timeId': #header
                continue

            timeId = int(timeId)
            count = int(count)
            
            on_demand_hour, reserve_upfront, reserve_hour = prices.get(instanceType)

            if market == 'OnDemand' and count > 0:
                od_vs_re[timeId][1] += count * on_demand_hour
                opt_vs_all_od[timeId][1] += count * on_demand_hour
            elif market == 'Reserved' and count > 0:
                od_vs_re[timeId][2] += count * reserve_upfront
                opt_vs_all_od[timeId][1] += count * reserve_upfront

                for i in range(timeId, min(timeId + 8760, max_t)):
                    od_vs_re[i][2] += count * reserve_hour
                    opt_vs_all_od[i][1] += count * reserve_hour
    
    print('Starting to iterate over total demand: ' + str((time.time() - start_time) / 60))
    opt_vs_all_od = get_all_od_cost(opt_vs_all_od, demand_path, prices)
    
    print('Starting to save files: ' + str((time.time() - start_time) / 60))  
    output1 = open('opt_vs_all_od.csv', 'w')
    writer1 = csv.writer(output1)
    writer1.writerow(['timeId', 'opt_cost', 'all_od_cost'])
    for line in opt_vs_all_od:
        writer1.writerow(line)
    output1.close()

    output2 = open('od_vs_re.csv', 'w')
    writer2 = csv.writer(output2)
    writer2.writerow(['timeId', 'od_cost', 'res_cost'])
    for line in od_vs_re:
        writer2.writerow(line)
    output2.close()
    print('Finished: ' + str((time.time() - start_time) / 60))

def get_prices(filename):
    prices = {}
    with open(filename, mode='r') as file:
        while True:
            line = file.readline()
            if not line: 
                break
            #line: Platform,Region,Instance,On.Demand_Hour,No.UP.1Y_Month,Part.UP.1Y_UP,Part.UP.1Y_Month,All.UP.1Y_UP,Part.UP.3Y_UP,Part.UP.3Y_Month,All.UP.3Y_UP
            line = line.split(',') 
            if line[0] == 'Platform': #header
                continue

            instanceType = line[2]
            on_demand_hour = float((line[3].split(' ')[0]).split('$')[1])
            reserve_upfront = float(line[5])
            reserve_hour = float(line[6])

            prices[instanceType] = [on_demand_hour, reserve_upfront, reserve_hour]
        return prices

if __name__ == "__main__":
    main()